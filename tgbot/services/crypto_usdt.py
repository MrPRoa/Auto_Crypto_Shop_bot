# - *- coding: utf- 8 - *-
import aiohttp
import asyncio
import random
from typing import Dict, Optional
import time
import json
import requests
from aiohttp import ClientSession
import configparser

try:
    import type_extension_package as type_extension
except ImportError:
    try:
        import typing_extensions_plus as type_extension
    except ImportError:
        # Fallback если библиотека не установлена
        type_extension = None

class CryptoUSDT:
    def __init__(self, wallet_address: str, private_key: str, bscscan_api_key: str, polygonscan_api_key: str = None, etherscan_api_key: str = None):
        self.wallet_address = wallet_address
        self.private_key = private_key
        self.bscscan_api_key = bscscan_api_key
        self.polygonscan_api_key = polygonscan_api_key or bscscan_api_key  # Используем тот же ключ если не указан отдельный
        self.etherscan_api_key = etherscan_api_key or bscscan_api_key  # Используем тот же ключ если не указан отдельный
        self.usdt_contract_bsc = "0x55d398326f99059ff775485246999027b3197955"  # USDT BEP-20 contract
        self.usdt_contract_polygon = "0xc2132D05D31c914a87C6611C10748AEb04B58e8F"  # USDT Polygon contract
        self.usdt_contract_erc20 = "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDT ERC-20 contract
        self.bsc_api_url = "https://api.bscscan.com/api"
        self.polygon_api_url = "https://api.polygonscan.com/api"
        self.etherscan_api_url = "https://api.etherscan.io/api"
        
    def generate_payment_amount(self, base_amount: float) -> float:
        """Генерирует уникальную сумму с копейками для идентификации платежа"""
        cents = random.randint(10, 99)
        return round(base_amount + (cents / 100), 2)
    
    async def get_recent_transactions(self, network: str = 'bsc') -> Optional[list]:
        """Получает последние транзакции USDT на кошелек"""
        try:
            if network == 'polygon':
                api_url = self.polygon_api_url
                contract = self.usdt_contract_polygon
                api_key = self.polygonscan_api_key
            elif network == 'erc20':
                api_url = self.etherscan_api_url
                contract = self.usdt_contract_erc20
                api_key = self.etherscan_api_key
            else:
                api_url = self.bsc_api_url
                contract = self.usdt_contract_bsc
                api_key = self.bscscan_api_key
                
            params = {
                'module': 'account',
                'action': 'tokentx',
                'contractaddress': contract,
                'address': self.wallet_address,
                'page': 1,
                'offset': 100,
                'startblock': 0,
                'endblock': 99999999,
                'sort': 'desc',
                'apikey': api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data['status'] == '1':
                            return data['result']
            return None
        except Exception as e:
            print(f"Error getting transactions for {network}: {e}")
            return None
    
    async def check_payment(self, expected_amount: float, network: str = 'bsc', time_limit: int = 3600) -> bool:
        """Проверяет поступление платежа на указанную сумму в течение time_limit секунд"""
        try:
            start_time = int(time.time())
            current_time = start_time
            
            transactions = await self.get_recent_transactions(network)
            if not transactions:
                return False
            
            # Ищем транзакцию с нужной суммой после start_time
            for tx in transactions:
                tx_time = int(tx['timeStamp'])
                if tx_time >= (start_time - 300):  # 5 минут до создания платежа
                    # Конвертируем из wei в USDT (18 decimals)
                    amount = float(tx['value']) / (10 ** int(tx['tokenDecimal']))
                    if abs(amount - expected_amount) < 0.01:  # точность до цента
                        return True
            
            return False
        except Exception as e:
            print(f"Error checking payment for {network}: {e}")
            return False
    
    async def get_balance(self, network: str = 'bsc') -> float:
        """Получает баланс USDT на кошельке"""
        try:
            if network == 'polygon':
                api_url = self.polygon_api_url
                contract = self.usdt_contract_polygon
                api_key = self.polygonscan_api_key
            elif network == 'erc20':
                api_url = self.etherscan_api_url
                contract = self.usdt_contract_erc20
                api_key = self.etherscan_api_key
            else:
                api_url = self.bsc_api_url
                contract = self.usdt_contract_bsc
                api_key = self.bscscan_api_key
                
            params = {
                'module': 'account',
                'action': 'tokenbalance',
                'contractaddress': contract,
                'address': self.wallet_address,
                'tag': 'latest',
                'apikey': api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data['status'] == '1':
                            # Конвертируем из wei в USDT
                            balance = float(data['result']) / (10 ** 18)
                            return round(balance, 2)
            return 0.0
        except Exception as e:
            print(f"Error getting balance for {network}: {e}")
            return 0.0
    
    def create_payment_info(self, amount_usd, network: str = 'bsc'):
        """Создать информацию для платежа"""
        # Генерируем уникальную сумму с копейками
        exact_usdt_amount = self.generate_payment_amount(amount_usd)
        
        if network == 'polygon':
            network_name = 'Polygon'
            contract = self.usdt_contract_polygon
        elif network == 'erc20':
            network_name = 'ERC-20 (Ethereum)'
            contract = self.usdt_contract_erc20
        else:
            network_name = 'BEP-20 (BSC)'
            contract = self.usdt_contract_bsc
        
        return {
            'wallet_address': self.wallet_address,
            'amount': exact_usdt_amount,
            'credit_amount': amount_usd,  # Зачисляется исходная сумма без копеек
            'network': network_name,
            'contract': contract
        }

class CryptoUSDTPolygon(CryptoUSDT):
    """Класс для работы с USDT в сети Polygon"""
    def __init__(self, wallet_address: str, private_key: str, polygonscan_api_key: str):
        super().__init__(wallet_address, private_key, "", polygonscan_api_key)
    
    async def get_recent_transactions(self) -> Optional[list]:
        """Получает последние транзакции USDT в сети Polygon"""
        return await super().get_recent_transactions('polygon')
    
    async def check_payment(self, expected_amount: float, time_limit: int = 3600) -> bool:
        """Проверяет поступление платежа в сети Polygon"""
        return await super().check_payment(expected_amount, 'polygon', time_limit)
    
    async def get_balance(self) -> float:
        """Получает баланс USDT в сети Polygon"""
        return await super().get_balance('polygon')
    
    def create_payment_info(self, amount_usd):
        """Создать информацию для платежа в сети Polygon"""
        return super().create_payment_info(amount_usd, 'polygon')

class CryptoUSDTERC20(CryptoUSDT):
    """Класс для работы с USDT в сети Ethereum (ERC-20)"""
    def __init__(self, wallet_address: str, private_key: str, etherscan_api_key: str):
        super().__init__(wallet_address, private_key, "", "", etherscan_api_key)
    
    async def get_recent_transactions(self) -> Optional[list]:
        """Получает последние транзакции USDT в сети Ethereum"""
        return await super().get_recent_transactions('erc20')
    
    async def check_payment(self, expected_amount: float, time_limit: int = 3600) -> bool:
        """Проверяет поступление платежа в сети Ethereum"""
        return await super().check_payment(expected_amount, 'erc20', time_limit)
    
    async def get_balance(self) -> float:
        """Получает баланс USDT в сети Ethereum"""
        return await super().get_balance('erc20')
    
    def create_payment_info(self, amount_usd):
        """Создать информацию для платежа в сети Ethereum"""
        return super().create_payment_info(amount_usd, 'erc20') 