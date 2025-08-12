package Config

import (
	"fmt"
	"os"
)

type Config struct {
	MiddlewarePort int
	RedisURL       string
	RedisPassword  string
	BybitAPIKey    string
	BybitAPISecret string
}

func GetConfigEnv() (*Config, error) {
	middlewarePort := getEnvInt("MIDDLEWARE_PORT", 6132)
	redisPort := getEnvInt("REDIS_PORT", 6379)
	redisPassword := os.Getenv("REDIS_PASSWORD")
	bybitKey := os.Getenv("BYBIT_API_KEY")
	bybitSecret := os.Getenv("BYBIT_API_SECRET")

	if redisPassword == "" || bybitKey == "" || bybitSecret == "" {
		return nil, fmt.Errorf("missing required environment variables")
	}

	return &Config{
		MiddlewarePort: middlewarePort,
		RedisURL:       fmt.Sprintf("redis://localhost:%d", redisPort),
		RedisPassword:  redisPassword,
		BybitAPIKey:    bybitKey,
		BybitAPISecret: bybitSecret,
	}, nil
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
