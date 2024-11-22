package handler

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/hyperledger/fabric-sdk-go/pkg/client/channel"
	fabric "github.com/righstar2020/br-cti-client/fabric-server/fabric"
	global "github.com/righstar2020/br-cti-client/fabric-server/global"
)
//POST /queryContract
func QueryContract(c *gin.Context){
	// 实现调用逻辑
	args:=c.PostFormArray("args")
	var params [][]byte
	for i := 0; i < len(args); i++ {
		params = append(params,[]byte(args[i]))
	}
	resp, err := fabric.InvokeChaincode(global.ChannelClient, global.ChaincodeName, c.PostForm("function"), params)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"result": resp})
}

//POST /invokeContract
func InvokeContract(c *gin.Context){
	// 实现调用逻辑
	args:=c.PostFormArray("args")
	var params [][]byte
	for i := 0; i < len(args); i++ {
		params = append(params,[]byte(args[i]))
	}
	resp, err := fabric.InvokeChaincode(global.ChannelClient, global.ChaincodeName, c.PostForm("function"), params)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"result": resp})
}

//POST /getTransactionNonce
func GetTransactionNonce(c *gin.Context){
	// 从请求中获取参数
	var msgData struct {
		UserID  string `json:"user_id"`
		TxSignature []byte `json:"tx_signature"`
	}

	if err := c.ShouldBindJSON(&msgData); err != nil {
		c.JSON(400, gin.H{"error": "参数错误"})
		return
	}

	// 调用链码生成随机数
	client, err := fabric.CreateChannelClient(global.FabricSDK)
	if err != nil {
		c.JSON(500, gin.H{"error": "创建通道客户端失败"})
		return
	}
	req := channel.Request{
		ChaincodeID: global.ChaincodeName,
		Fcn:         "getTransactionNonce",
		Args:        [][]byte{[]byte(msgData.UserID), msgData.TxSignature},
	}
	resp, err := client.Execute(req)
	if err != nil {
		c.JSON(500, gin.H{"error": "执行链码失败:" + err.Error()})
		return
	}
	nonce := string(resp.Payload)

	c.JSON(200, gin.H{
		"code": 200,
		"message": "success",
		"data": gin.H{
			"nonce": nonce,
		},
	})
}
