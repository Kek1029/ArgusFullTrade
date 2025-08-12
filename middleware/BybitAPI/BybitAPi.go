package BybitAPI

import (
	"context"
	"errors"
	"fmt"
	"middleware/Config"

	bybit "github.com/bybit-exchange/bybit.go.api"
)

type OrderRequest struct {
	Symbol   string
	Side     string
	Quantity float64
	Price    float64
	Type     string
}

type OrderResponse struct {
	OrderID string
	Status  string
}

type Balance struct {
	Asset  string
	Amount float64
}

type MarketData struct {
	Symbol string
	Price  float64
}

type BybitAPI interface {
	GetBalance() ([]Balance, error)
	PlaceOrder(req OrderRequest) (OrderResponse, error)
	CancelOrder(orderID string) error
	GetOrderStatus(orderID string) (OrderResponse, error)
	GetMarketData(symbol string) (MarketData, error)
}

type bybitImpl struct {
	client bybit.Client
}

func (b bybitImpl) GetBalance() ([]Balance, error) {
	params := map[string]interface{}{"accountType": "UNFIED"}
	resp, err := b.client.NewUtaBybitServiceWithParams(params).GetAllCoinsBalance(context.Background())
	if err != nil {
		return nil, err
	}

	if resp.RetCode != 0 {
		return nil, errors.New(resp.RetMsg)
	}

	rawList, ok := resp.Result.(map[string]interface{})["balanceList"]
	if !ok {
		return nil, fmt.Errorf("missing balanceList in response")
	}

	list, ok := rawList.([]interface{})
	if !ok {
		return nil, fmt.Errorf("balanceList is not a slice")
	}

	var balances []Balance
	for _, item := range list {
		entry, ok := item.(map[string]interface{})
		if !ok {
			continue
		}
		asset, _ := entry["coin"].(string)
		amountStr, _ := entry["availableBalance"].(string)
		var amount float64
		fmt.Sscanf(amountStr, "%f", &amount)

		balances = append(balances, Balance{
			Asset:  asset,
			Amount: amount,
		})
	}

	return balances, nil

}

func (b bybitImpl) PlaceOrder(req OrderRequest) (OrderResponse, error) {
	//TODO implement me
	panic("implement me")
}

func (b bybitImpl) CancelOrder(orderID string) error {
	//TODO implement me
	panic("implement me")
}

func (b bybitImpl) GetOrderStatus(orderID string) (OrderResponse, error) {
	//TODO implement me
	panic("implement me")
}

func (b bybitImpl) GetMarketData(symbol string) (MarketData, error) {
	//TODO implement me
	panic("implement me")
}

func New(cfg *Config.Config) BybitAPI {
	return &bybitImpl{
		client: *bybit.NewBybitHttpClient(cfg.BybitAPIKey, cfg.BybitAPISecret, bybit.WithBaseURL(bybit.TESTNET)),
	}
}
