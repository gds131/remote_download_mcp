def join_paths(base_path: str, custom_path: str = None) -> str:
    """拼接路径，处理多余的'/'
    
    Args:
        base_path: 基础路径
        custom_path: 自定义路径
    
    Returns:
        str: 拼接后的路径
    """
    if custom_path is None:
        return base_path
    
    # 移除基础路径末尾的'/'
    base_path = base_path.rstrip('/')
    # 移除自定义路径开头的'/'
    custom_path = custom_path.lstrip('/')
    
    # 拼接路径
    return f"{base_path}/{custom_path}"
