package Config

import (
	"fmt"
	"os"
)

type Config struct {
	FrontendCorePort       int
	BackendCorePort        int
	MiddlewareCorePort     int
	MiddlewareFrontendPort int
	MiddlewareBybitPort    int
	MiddlewareBackendPort  int
	MiddlewareRedisPort    int

	RedisHost     string
	RedisPort     int
	RedisURL      string
	RedisPassword string

	BybitAPIKey    string
	BybitAPISecret string
}

func GetConfigEnv() (*Config, error) {
	cfg := &Config{
		MiddlewareCorePort:     getEnvInt("MIDDLEWARE_CORE_PORT", 6132),
		MiddlewareFrontendPort: getEnvInt("MIDDLEWARE_FRONTEND_PORT", 6133),
		MiddlewareBackendPort:  getEnvInt("MIDDLEWARE_BACKEND_PORT", 6134),
		MiddlewareBybitPort:    getEnvInt("MIDDLEWARE_BYBIT_PORT", 6135),
		MiddlewareRedisPort:    getEnvInt("MIDDLEWARE_REDIS_PORT", 6136),

		FrontendCorePort: getEnvInt("FRONTEND_CORE_PORT", 6459),
		BackendCorePort:  getEnvInt("BACKEND_CORE_PORT", 6521),

		RedisHost:     "localhost",
		RedisPort:     getEnvInt("REDIS_PORT", 6379),
		RedisPassword: os.Getenv("REDIS_PASSWORD"),

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
	return nil
}

func (cfg *Config) LogSummary() {
	fmt.Println("Config loaded:")
	fmt.Printf("  Middleware Core Port: %d\n", cfg.MiddlewareCorePort)
	fmt.Printf("  Redis URL: %s\n", cfg.RedisURL)
	fmt.Printf("  Bybit Key: %s\n", mask(cfg.BybitAPIKey))
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
