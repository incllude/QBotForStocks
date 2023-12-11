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
bot = MarketBot('./hours', './moex_data_hours', 100000)
bot.load_model('./trained_model')

output = bot.get_states(datasets)
actions = get_actions(output, datasets)
```

```output``` - объект из библиотеки **Qlib**

```actions``` - готовый для дальнешего использования объект