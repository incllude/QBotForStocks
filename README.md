# QBotForStocks

Код для установки библиотеки **Qlib**:
```
!git clone https://github.com/microsoft/qlib.git
!cd qlib && pip install . -q
```

```MarketBot``` - основной объект

Пример работы:
```
bot = MarketBot('/kaggle/working/hours', '/kaggle/working/moex_data_hours')
bot.load_model('/kaggle/input/qlib-model-saving/trained_model')

output = bot.get_states(datasets)
actions = get_actions(output, datasets)
```

```output``` - объект из библиотеки **Qlib**
```actions``` - уже готовый для дальнешего использования объект