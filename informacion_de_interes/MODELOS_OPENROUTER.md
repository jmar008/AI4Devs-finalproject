# 🤖 Modelos Gratuitos de OpenRouter - Actualizado 2025

## Configuración Actual del Sistema

### Modelo Principal

- **DeepSeek R1** (`deepseek/deepseek-r1:free`)
  - Context: 163,840 tokens
  - Mejor modelo razonamiento disponible gratis
  - Ideal para consultas complejas de stock

### Modelos Fallback (22 modelos)

#### Tier 1: Modelos Grandes (70B+) - Máxima Calidad

1. **Llama 3.3 70B** - `meta-llama/llama-3.3-70b-instruct:free` (131k tokens)
2. **DeepSeek R1 Distill 70B** - `deepseek/deepseek-r1-distill-llama-70b:free` (8k tokens)
3. **Qwen 2.5 72B** - `qwen/qwen-2.5-72b-instruct:free` (32k tokens)
4. **Hermes 3 405B** - `nousresearch/hermes-3-llama-3.1-405b:free` (131k tokens)

#### Tier 2: Modelos Medianos (20-40B) - Balance Calidad/Velocidad

5. **Qwen 2.5 Coder 32B** - `qwen/qwen-2.5-coder-32b-instruct:free` (32k tokens)
6. **Mistral Small 3.2 24B** - `mistralai/mistral-small-3.2-24b-instruct:free` (131k tokens)
7. **Qwen 2.5 VL 32B** - `qwen/qwen-2.5-vl-32b-instruct:free` (16k tokens)
8. **Dolphin Mistral 24B** - `cognitivecomputations/dolphin-mistral-24b-venice-edition:free` (32k tokens)

#### Tier 3: Familia DeepSeek - Especializado

9. **DeepSeek V3.1** - `deepseek/deepseek-chat-v3.1:free` (163k tokens)
10. **DeepSeek V3 0324** - `deepseek/deepseek-chat-v3-0324:free` (163k tokens)
11. **DeepSeek R1 0528** - `deepseek/deepseek-r1-0528:free` (163k tokens)

#### Tier 4: Modelos Especializados

12. **Google Gemini 2.0 Flash** - `google/gemini-2.0-flash-exp:free` (1M tokens!)
13. **Qwen3 Coder 480B** - `qwen/qwen3-coder:free` (262k tokens)
14. **MiniMax M2** - `minimax/minimax-m2:free` (204k tokens)

#### Tier 5: Modelos Rápidos (8-14B) - Alta Velocidad

15. **Llama 3.3 8B** - `meta-llama/llama-3.3-8b-instruct:free` (128k tokens)
16. **Mistral Nemo** - `mistralai/mistral-nemo:free` (131k tokens)
17. **Gemma 3 12B** - `google/gemma-3-12b-it:free` (32k tokens)
18. **Qwen3 14B** - `qwen/qwen3-14b:free` (40k tokens)

#### Tier 6: Modelos Ligeros - Respaldo

19. **Gemma 2 9B** - `google/gemma-2-9b-it:free` (8k tokens)
20. **Llama 3.2 3B** - `meta-llama/llama-3.2-3b-instruct:free` (131k tokens)
21. **Mistral 7B** - `mistralai/mistral-7b-instruct:free` (32k tokens)

## Otros Modelos Disponibles (No en Config)

### Modelos Adicionales Potentes

- **TNG DeepSeek R1T2 Chimera** - `tngtech/deepseek-r1t2-chimera:free` (163k)
- **Z.AI GLM 4.5 Air** - `z-ai/glm-4.5-air:free` (131k)
- **Qwen3 235B A22B** - `qwen/qwen3-235b-a22b:free` (40k)
- **Meta Llama 4 Maverick** - `meta-llama/llama-4-maverick:free` (128k)
- **Meta Llama 4 Scout** - `meta-llama/llama-4-scout:free` (128k)
- **Microsoft MAI DS R1** - `microsoft/mai-ds-r1:free` (163k)

### Modelos Especializados

- **MoonshotAI Kimi Dev 72B** - `moonshotai/kimi-dev-72b:free` (131k)
- **MoonshotAI Kimi K2** - `moonshotai/kimi-k2:free` (32k)
- **Meituan LongCat Flash** - `meituan/longcat-flash-chat:free` (131k)
- **Tongyi DeepResearch 30B** - `alibaba/tongyi-deepresearch-30b-a3b:free` (131k)
- **NVIDIA Nemotron Nano 9B** - `nvidia/nemotron-nano-9b-v2:free` (128k)

### Modelos de Código

- **DeepSeek R1 0528 Qwen3 8B** - `deepseek/deepseek-r1-0528-qwen3-8b:free` (131k)
- **Mistral Devstral Small** - `mistralai/devstral-small-2505:free` (32k)
- **Agentica Deepcoder 14B** - `agentica-org/deepcoder-14b-preview:free` (96k)

### Modelos Pequeños/Rápidos

- **OpenAI GPT-OSS 20B** - `openai/gpt-oss-20b:free` (131k)
- **Google Gemma 3 4B** - `google/gemma-3-4b-it:free` (32k)
- **Google Gemma 3n 2B** - `google/gemma-3n-e2b-it:free` (8k)
- **Google Gemma 3n 4B** - `google/gemma-3n-e4b-it:free` (8k)
- **Qwen3 4B** - `qwen/qwen3-4b:free` (40k)
- **Qwen3 8B** - `qwen/qwen3-8b:free` (40k)

### Modelos Multilingües/Especializados

- **Shisa AI V2 Llama 3.3 70B** - `shisa-ai/shisa-v2-llama3.3-70b:free` (32k)
- **Tencent Hunyuan A13B** - `tencent/hunyuan-a13b-instruct:free` (32k)
- **ArliAI QwQ 32B** - `arliai/qwq-32b-arliai-rpr-v1:free` (32k)

## Estrategia de Selección

### Para Generación de Vehículos (1000+)

**Prioridad**: Velocidad y disponibilidad

1. DeepSeek R1 (principal)
2. Llama 3.3 70B
3. Qwen 2.5 72B
4. Mistral Small 24B
5. Llama 3.3 8B (rápido)

### Para Chat con IA

**Prioridad**: Calidad de respuesta y contexto

1. DeepSeek R1 (163k context)
2. Gemini 2.0 Flash (1M context!)
3. Hermes 3 405B (más potente)
4. DeepSeek V3.1
5. Llama 3.3 70B

### Para Análisis de Código

**Prioridad**: Especialización

1. Qwen3 Coder 480B
2. Qwen 2.5 Coder 32B
3. Mistral Devstral Small
4. Agentica Deepcoder 14B

## Ventajas del Sistema Actualizado

### Antes (12 modelos)

- Modelos antiguos (2023-2024)
- Máximo: Hermes 3 405B
- Promedio: 7-8B parámetros
- Context: 8k-131k tokens

### Ahora (23 modelos)

- Modelos nuevos (2025)
- Incluye: DeepSeek R1, Llama 3.3, Qwen 2.5, Gemini 2.0
- Promedio: 20-40B parámetros
- Context: hasta 1M tokens (Gemini)

## Capacidad Estimada

Con 23 modelos de fallback:

| Vehículos | Tiempo  | Modelos Usados | Tasa Éxito |
| --------- | ------- | -------------- | ---------- |
| 100       | ~1 min  | 1-3            | 99%        |
| 500       | ~5 min  | 3-8            | 95%+       |
| 1000      | ~10 min | 5-12           | 90%+       |
| 2000      | ~20 min | 8-18           | 85%+       |
| 5000+     | ~50 min | Todos          | 80%+       |

## Recomendaciones de Uso

### Producción

```python
DEEPSEEK_MODEL = 'deepseek/deepseek-r1:free'
```

- Mejor balance calidad/velocidad
- Excelente razonamiento
- 163k context

### Testing/Dev

```python
DEEPSEEK_MODEL = 'meta-llama/llama-3.3-8b-instruct:free'
```

- Muy rápido
- 128k context
- Buena calidad

### Máxima Calidad (Chat)

```python
DEEPSEEK_MODEL = 'google/gemini-2.0-flash-exp:free'
```

- 1M tokens de contexto
- Excelente para análisis complejos
- Puede procesar todo el stock

### Máxima Velocidad (Bulk)

```python
DEEPSEEK_MODEL = 'google/gemma-2-9b-it:free'
```

- Muy rápido
- Bueno para generación masiva
- Menor calidad pero suficiente

## Actualización Futura

Para añadir nuevos modelos, verificar en:

- https://openrouter.ai/models?q=free
- Buscar modelos con `$0` en input y output
- Preferir modelos con mayor context window
- Priorizar modelos recientes (2025)

## Notas Importantes

1. **Rate Limiting**: Los modelos gratuitos tienen límites de tasa
2. **Disponibilidad**: Puede variar según demanda
3. **Fallback**: El sistema automáticamente rotará entre modelos
4. **Context**: Mayor context = mejor para análisis de stock completo
5. **Actualización**: OpenRouter añade nuevos modelos mensualmente

---

**Última actualización**: Octubre 2025
**Versión**: 3.0 - Lista Expandida 2025
