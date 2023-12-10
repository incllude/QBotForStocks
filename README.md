# QBotForStocks

Код для установки библиотеки **Qlib**:
```
!git clone https://github.com/microsoft/qlib.git
!cd qlib && pip install . -q
```

```MarketBot``` - основной объект

[Model Training](model_training.ipynb) - пример тренировки модели для бота

Пример работы c ботом:
```
bot = MarketBot('/kaggle/working/hours', '/kaggle/working/moex_data_hours')
bot.load_model('/kaggle/input/qlib-model-saving/trained_model')

output = bot.get_states(datasets)
actions = get_actions(output, datasets)
```

```output``` - объект из библиотеки **Qlib**

```actions``` - готовый для дальнешего использования объект
