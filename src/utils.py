def join_paths(base_path, user_path):
    """
    拼接路径，处理多余的"/"
    
    Args:
        base_path: 基础路径（如下载器配置中的save_path）
        user_path: 用户传递的路径
    
    Returns:
        拼接后的完整路径
    """
    final_path = base_path
    if user_path:
        # 移除基础路径末尾的"/"
        final_path = final_path.rstrip('/')
        # 移除用户路径开头的"/"
        user_path = user_path.lstrip('/')
        # 如果用户路径不为空，拼接路径
        if user_path:
            final_path = f"{final_path}/{user_path}"
    return final_path