# Models Directory

Esta pasta contém a estrutura para armazenamento de modelos de machine learning.

## Estrutura

```
models/
├── trained/          # Modelos finalizados prontos para uso
├── checkpoints/      # Checkpoints durante o treinamento
└── .gitkeep         # Mantém a estrutura no git
```

## Uso

### Treinamento
- Execute `python legacy/quick_train.py` para treinar um novo modelo
- Os modelos serão salvos automaticamente em `trained/` com timestamp
- O último modelo será salvo como `trained_fire_detection_model.h5` para facilitar os testes

### Teste
- Execute `python legacy/test_model.py` para testar o modelo treinado
- O script procura automaticamente por `models/trained/trained_fire_detection_model.h5`

## Nota sobre Git

**Os modelos treinados NÃO são incluídos no repositório** por serem arquivos grandes e específicos do ambiente local.

Cada desenvolvedor deve:
1. Treinar seus próprios modelos localmente
2. Os modelos ficam em `models/trained/` (ignorado pelo git)
3. Compartilhar apenas o código de treinamento e teste

## Vantagens desta abordagem

✅ **Repositório leve** - Sem arquivos grandes de modelos
✅ **Flexibilidade** - Cada ambiente pode ter modelos otimizados
✅ **Controle de versão limpo** - Apenas código no git
✅ **Reprodutibilidade** - Código de treinamento versionado
✅ **Organização** - Estrutura clara e profissional
