import requests
from blockchain.fabric import env_vars
from blockchain.fabric.tx import createSignTransaction,createTransaction
import logging
def uploadCTIToBlockchain(wallet_id:str, password:str, cti_data:dict)->tuple[str,bool]:
    """
    执行智能合约上传CTI数据到区块链
    params:
        wallet_id: 钱包ID
        password: 钱包密码
        cti_data: CTI数据
    return:
        result: 结果信息
        success: 是否成功
    """
    try:
        # 创建签名交易
        #tx_msg = createSignTransaction(wallet_id, password, cti_data)
        # 暂时不需要签名
        # 创建交易消息
        tx_msg = createTransaction(wallet_id, password, cti_data)
        
        # 将交易数据转换为bytes
        tx_msg_data = {
            "user_id": str(tx_msg["user_id"]),
            "tx_data": tx_msg["tx_data"], 
            "nonce": "",
            "tx_signature": bytes(tx_msg["tx_signature"], 'utf-8'),
            "nonce_signature": bytes(tx_msg["nonce_signature"], 'utf-8')
        }
        
        # 发送POST请求到fabric-server
        response = requests.post(env_vars.fabricServerHost + env_vars.fabricServerApi['cti']['registerCtiInfo'],
                               json=tx_msg_data)
        logging.info("uploadCTIToBlockchain response:"+str(response.json()))
        if response.status_code != 200:
            return response.json()['error'], False
            
        return response.json()['data'], True
        
    except Exception as e:
        return str(e), False