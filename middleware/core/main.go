package main

import (
	"fmt"
	"middleware_core/Config"
	"middleware_core/RabbitAPI"
)

func main() {
	cfg, err := Config.GetConfigEnv()
	if err != nil {
		panic(err)
	}

	globalBroker := RabbitAPI.NewURL(cfg.RabbitGlobalURL)
	localBroker := RabbitAPI.NewURL(cfg.RabbitLocalURL)

	// Подписка на глобальные команды
	binding := RabbitAPI.QueueBinding{
		Exchange:   cfg.ExchangeName,
		RoutingKey: cfg.MiddlewareRoutingKey,
		QueueName:  cfg.MiddlewareQueue,
		Durable:    true,
		AutoDelete: false,
	}

	err = globalBroker.Subscribe(binding, func(msg RabbitAPI.BrokerMessage) error {
		fmt.Println("Received global message:")
		fmt.Println("Type:", msg.Type)
		fmt.Println("Payload:", string(msg.Payload))
		return routeToLocal(localBroker, cfg, msg)
	})
	if err != nil {
		panic(err)
	}

	select {} // блокируем main
}

func routeToLocal(local RabbitAPI.IRabbitAPI, cfg *Config.Config, msg RabbitAPI.BrokerMessage) error {
	var targetKey string

	switch msg.Type {
	case "order.bybit":
		targetKey = cfg.BybitRoutingKey
	case "order.backend":
		targetKey = cfg.BackendRoutingKey
	case "order.redis":
		targetKey = cfg.RedisRoutingKey
	case "order.frontend":
		targetKey = cfg.FrontendRoutingKey
	default:
		fmt.Println("Unknown message type:", msg.Type)
		return nil
	}

	err := local.Publish(cfg.ExchangeName, targetKey, msg)
	if err != nil {
		fmt.Println("Failed to route to local:", err)
		return err
	}

	fmt.Println("Routed to local:", targetKey)
	return nil
}
