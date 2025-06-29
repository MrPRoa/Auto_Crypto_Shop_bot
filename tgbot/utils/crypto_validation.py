# - *- coding: utf- 8 - *-
import re
import binascii

def is_valid_private_key_hex(private_key: str) -> bool:
    """Проверяет является ли строка валидным приватным ключом в hex формате (64 символа)"""
    if not private_key:
        return False
    
    # Убираем префикс 0x если есть
    if private_key.startswith('0x'):
        private_key = private_key[2:]
    
    # Проверяем длину (должно быть 64 символа для 256-битного ключа)
    if len(private_key) != 64:
        return False
    
    # Проверяем что все символы - валидные hex символы
    try:
        int(private_key, 16)
        return True
    except ValueError:
        return False

def is_valid_private_key_wif(private_key: str) -> bool:
    """Проверяет является ли строка валидным приватным ключом в WIF формате"""
    if not private_key:
        return False
    
    # WIF ключи обычно начинаются с определенных символов и имеют определенную длину
    # Для Bitcoin mainnet: начинается с '5', 'K' или 'L' и длина 51-52 символа
    # Для testnet: начинается с '9' или 'c'
    if len(private_key) < 51 or len(private_key) > 52:
        return False
    
    # Базовая проверка на валидные символы Base58
    valid_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    return all(c in valid_chars for c in private_key)

def validate_private_key_for_network(private_key: str, network: str = 'bsc') -> dict:
    """
    Валидирует приватный ключ для конкретной сети
    
    Args:
        private_key: Приватный ключ для проверки
        network: Сеть ('bsc', 'polygon', 'erc20')
    
    Returns:
        dict: {'valid': bool, 'error': str, 'network': str}
    """
    if not private_key or private_key.strip() == "":
        return {
            'valid': False,
            'error': f'Приватный ключ для сети {network.upper()} не задан',
            'network': network
        }
    
    # Убираем пробелы
    private_key = private_key.strip()
    
    # Для Ethereum-совместимых сетей (BSC, Polygon, ERC-20) используем hex формат
    if network.lower() in ['bsc', 'polygon', 'erc20', 'ethereum']:
        if is_valid_private_key_hex(private_key):
            return {
                'valid': True,
                'error': None,
                'network': network
            }
        else:
            return {
                'valid': False,
                'error': f'Неверный формат приватного ключа для сети {network.upper()}. Ожидается hex формат (64 символа)',
                'network': network
            }
    
    # Для других сетей можно добавить дополнительные проверки
    return {
        'valid': False,
        'error': f'Неподдерживаемая сеть: {network}',
        'network': network
    }

def validate_all_crypto_keys(config) -> dict:
    """
    Проверяет все приватные ключи в конфигурации
    
    Returns:
        dict: {'valid': bool, 'errors': list, 'details': dict}
    """
    errors = []
    details = {}
    
    if not hasattr(config, 'crypto_private_key') or not config.crypto_private_key:
        errors.append("Приватный ключ не задан в конфигурации")
        return {
            'valid': False,
            'errors': errors,
            'details': details
        }
    
    # Проверяем ключ для каждой поддерживаемой сети
    networks = ['bsc', 'polygon', 'erc20']
    
    for network in networks:
        result = validate_private_key_for_network(config.crypto_private_key, network)
        details[network] = result
        
        if not result['valid']:
            errors.append(f"{network.upper()}: {result['error']}")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'details': details
    } 