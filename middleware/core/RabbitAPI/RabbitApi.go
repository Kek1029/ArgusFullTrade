package RabbitAPI

import (
	"encoding/json"
	"log"

	amqp "github.com/rabbitmq/amqp091-go"
)

type IRabbitAPI interface {
	Publish(exchange, routingKey string, msg BrokerMessage) error
	Subscribe(binding QueueBinding, handler func(BrokerMessage) error) error
	Close() error
}

type rabbitClient struct {
	conn    *amqp.Connection
	channel *amqp.Channel
	config  BrokerConfig
}

func (r *rabbitClient) Publish(exchange, routingKey string, msg BrokerMessage) error {
	body, err := json.Marshal(msg)
	if err != nil {
		return err
	}

	return r.channel.Publish(
		exchange,
		routingKey,
		false,
		false,
		amqp.Publishing{
			ContentType: "application/json",
			Body:        body,
		},
	)
}

func (r *rabbitClient) Subscribe(binding QueueBinding, handler func(BrokerMessage) error) error {
	_, err := r.channel.QueueDeclare(
		binding.QueueName,
		binding.Durable,
		binding.AutoDelete,
		false,
		false,
		nil,
	)
	if err != nil {
		return err
	}

	err = r.channel.QueueBind(
		binding.QueueName,
		binding.RoutingKey,
		binding.Exchange,
		false,
		nil,
	)
	if err != nil {
		return err
	}

	msgs, err := r.channel.Consume(
		binding.QueueName,
		"",
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		return err
	}

	go func() {
		for d := range msgs {
			var msg BrokerMessage
			if err := json.Unmarshal(d.Body, &msg); err == nil {
				handler(msg)
			}
		}
	}()

	return nil
}

func (r *rabbitClient) Close() error {
	if err := r.channel.Close(); err != nil {
		return err
	}
	return r.conn.Close()
}

func New(MQURL string) IRabbitAPI {
	return NewURL(MQURL)
}

func NewURL(url string) IRabbitAPI {
	conn, err := amqp.Dial(url)
	if err != nil {
		log.Fatalf("RabbitMQ connection failed: %v", err)
	}

	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("RabbitMQ channel failed: %v", err)
	}

	return &rabbitClient{
		conn:    conn,
		channel: ch,
		config:  BrokerConfig{URL: url},
	}
}

type BrokerConfig struct {
	URL      string
	Host     string
	Port     int
	Username string
	Password string
	VHost    string
}

type QueueBinding struct {
	Exchange   string
	RoutingKey string
	QueueName  string
	Durable    bool
	AutoDelete bool
}

type BrokerMessage struct {
	Type    string            `json:"type"`
	Payload json.RawMessage   `json:"payload"`
	Meta    map[string]string `json:"meta,omitempty"`
}
