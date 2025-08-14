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
    cfg.LogSummary()
	globalBroker := RabbitAPI.NewURL(cfg.RabbitGlobalURL)

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
        return nil
    })
    if err != nil {
        fmt.Println("Subscribe error:", err)
        panic(err)
    }


	select {} // блокируем main
}
