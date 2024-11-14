package global

import (
	"github.com/hyperledger/fabric-sdk-go/pkg/client/channel"
	"github.com/hyperledger/fabric-sdk-go/pkg/client/ledger"
	"github.com/hyperledger/fabric-sdk-go/pkg/fabsdk"
)
var (
	FabricSDK *fabsdk.FabricSDK
	ChannelClient *channel.Client
	LedgerClient *ledger.Client
)