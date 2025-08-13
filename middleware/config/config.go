package config

import (
	"fmt"
	"os"
)

type Config struct {
	// Frontend
	FrontendCorePort     int
	FrontendTelegramPort int
	FrontendWebPort      int
	TelegramBotToken     string

	// Middleware
	MiddlewareCorePort     int
	MiddlewareFrontendPort int
	MiddlewareBybitPort    int
	MiddlewareBackendPort  int
	MiddlewareRedisPort    int

	// Backend
	BackendCorePort       int
	BackendMiddlewarePort int
	BackendRedisPort      int

	// Redis
	RedisHost     string
	RedisPort     int
	RedisURL      string
	RedisPassword string

	// RabbitMQ
	RabbitMQPort         int
	RabbitMQURL          string
	ExchangeName         string
	MiddlewareQueue      string
	MiddlewareRoutingKey string

	FrontendRoutingKey string
	BybitRoutingKey    string
	RedisRoutingKey    string
	BackendRoutingKey  string

	// Bybit
	BybitAPIKey    string
	BybitAPISecret string
}

func GetConfigEnv() (*Config, error) {
	cfg := &Config{
		// Frontend
		FrontendCorePort:     getEnvInt("FRONTEND_CORE_PORT", 6459),
		FrontendTelegramPort: getEnvInt("FRONTEND_TELEGRAM_PORT", 6541),
		FrontendWebPort:      getEnvInt("FRONTEND_WEB_PORT", 5713),
		TelegramBotToken:     os.Getenv("TELEGRAM_BOT_TOKEN"),

		// Middleware
		MiddlewareCorePort:     getEnvInt("MIDDLEWARE_CORE_PORT", 6132),
		MiddlewareFrontendPort: getEnvInt("MIDDLEWARE_FRONTEND_PORT", 6133),
		MiddlewareBackendPort:  getEnvInt("MIDDLEWARE_BACKEND_PORT", 6134),
		MiddlewareBybitPort:    getEnvInt("MIDDLEWARE_BYBIT_PORT", 6135),
		MiddlewareRedisPort:    getEnvInt("MIDDLEWARE_REDIS_PORT", 6136),

		// Backend
		BackendCorePort:       getEnvInt("BACKEND_CORE_PORT", 6521),
		BackendMiddlewarePort: getEnvInt("BACKEND_MIDDLEWARE_PORT", 6522),
		BackendRedisPort:      getEnvInt("BACKEND_REDIS_PORT", 6523),

		// Redis
		RedisHost:     "localhost",
		RedisPort:     getEnvInt("REDIS_PORT", 6379),
		RedisPassword: os.Getenv("REDIS_PASSWORD"),

		// RabbitMQ
		RabbitMQPort:         getEnvInt("RABBITMQ_PORT", 15672),
		RabbitMQURL:          "amqp://guest:guest@rabbitmq:5672/",
		ExchangeName:         "events",
		MiddlewareQueue:      "route.middleware",
		MiddlewareRoutingKey: "route.middleware",

		FrontendRoutingKey: "order.frontend",
		BybitRoutingKey:    "order.bybit",
		RedisRoutingKey:    "order.redis",
		BackendRoutingKey:  "order.backend",

		// Bybit
		BybitAPIKey:    os.Getenv("BYBIT_API_KEY"),
		BybitAPISecret: os.Getenv("BYBIT_API_SECRET"),
	}

	cfg.RedisURL = fmt.Sprintf("redis://%s:%d", cfg.RedisHost, cfg.RedisPort)

	if err := cfg.Validate(); err != nil {
		return nil, err
	}

	return cfg, nil
}

func (cfg *Config) Validate() error {
	if cfg.RedisPassword == "" {
		return fmt.Errorf("missing REDIS_PASSWORD")
	}
	if cfg.BybitAPIKey == "" || cfg.BybitAPISecret == "" {
		return fmt.Errorf("missing BYBIT_API_KEY or BYBIT_API_SECRET")
	}
	if cfg.TelegramBotToken == "" {
		return fmt.Errorf("missing TELEGRAM_BOT_TOKEN")
	}
	return nil
}

func (cfg *Config) LogSummary() {
	fmt.Println("Config loaded:")
	fmt.Printf("  Middleware Core Port: %d\n", cfg.MiddlewareCorePort)
	fmt.Printf("  Redis URL: %s\n", cfg.RedisURL)
	fmt.Printf("  RabbitMQ URL: %s\n", cfg.RabbitMQURL)
	fmt.Printf("  Exchange: %s\n", cfg.ExchangeName)
	fmt.Printf("  Bybit Key: %s\n", mask(cfg.BybitAPIKey))
	fmt.Printf("  Telegram Token: %s\n", mask(cfg.TelegramBotToken))
}

func mask(s string) string {
	if len(s) <= 4 {
		return "****"
	}
	return s[:4] + "****"
}

func getEnvInt(key string, defaultVal int) int {
	val := os.Getenv(key)
	if val == "" {
		return defaultVal
	}
	var i int
	_, err := fmt.Sscanf(val, "%d", &i)
	if err != nil {
		return defaultVal
	}
	return i
}
