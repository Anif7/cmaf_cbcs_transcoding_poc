def convert_to_ffmpeg_bitrate(value) -> str:
    if isinstance(value, int):
        return f"{value // 1000}k"
    return str(value)
