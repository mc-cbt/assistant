# Modelfile for Qwen 3.6 MLX (Better Results)

```
FROM qwen3.6:35b-mlx

# Expand context to 32k for multi-file reading
PARAMETER num_ctx 32768
PARAMETER temperature 0.2 
```
