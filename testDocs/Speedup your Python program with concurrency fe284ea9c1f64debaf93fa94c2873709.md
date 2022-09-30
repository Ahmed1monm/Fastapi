# Speedup your Python program with concurrency

Link: https://realpython.com/python-concurrency/
Status: Reading
Type: Article

# What is concurrency:

### Threads, Tasks and Process:

All of them can be stopped at point and CPU switches to different one.

-. `[Threading](https://realpython.com/intro-to-python-threading/)`and `asyncio` both run on a single processor and therefore only run one at a time. They just cleverly find ways to take turns to speed up the overall process. Even though they don’t run different trains of thought simultaneously, we still call this concurrency.

### Threading uses ***Pre-emptive Multitasking***

دي بتقطع تنفيذ الثريد في أي نقطة وتنقل على آخر ودي ليها ميزة وعيب 

- الميزة: انك مش محتاج تعمل حاجة ف الكود عشان تنقل على تاسك تاني هو هينقل لوحده
- العيب: انك بتقطع التاسك في أي وقت حتى في السطر الواحد  `x=x+1`

### asyncio uses ***Cooperative Multithreading***

دي بتستنى التاسك يقول هو مستعد يتحول يتنقل امتى عشان البروسيسور يبدأ ينقل

- الميزة: ان التاسك مش هيتقطع ف أي وقت وانت عارف امتى هيحصلك سويتش
- العيب: انك محتاج تحط حاجة ف الكود عشان تعرف البروسيسور انه يسويتش عادي

# What is parallelism?

### Multiprocessing:

بايثون بتعمل بروسيس جديدة بيكون لها الموارد بتاعتها وكل واحدة بتشتغل على منفذ اوامر خاص بيها. فدا معناه انه كل بروسيس قادرة تشتغل على كور خاص بيها ودا معناه ان البروسيسيز كلها هتكون شغالة في نفس الوقت

| Concurrency Type | Switching Decision | Number of Processors |
| --- | --- | --- |
| Pre-emptive multitasking (threading) | The operating system decides when to switch tasks external to Python. |                1 |
| Cooperative multitasking (asyncio) | The tasks decide when to give up control. |                1 |
| Multiprocessing (multiprocessing) | The processes all run at the same time on different processors. |             Many |

# ****When Is Concurrency Useful?****

There is 2 types of problems :

- CPU-bound
- I/O-bound

في أحيان كثيرة بيكون البرنامج بيتعامل مع حاجات ابطأ من البروسيسور لذلك البروسيسور بيكون عطلان زي الفايل سيستم والانترنت مثلا. دي كدا المشكلة التانية 

احيانا بيكون البروسيسور عمل حاجة ف تعليمة معينة ولسه مخلصتش بس في حاجات واقفه فانت بتخليها تشتغل بالتوازي يعني مش هستنى البروسيسور يخلص كل التعليمة مرة واحدة وأبدأ ادخل على اللي بعدها 

| I/O-Bound Process | CPU-Bound Process |
| --- | --- |
| Your program spends most of its time talking to a slow device, like a network connection, a hard drive, or a printer. | You program spends most of its time doing CPU operations. |
| Speeding it up involves overlapping the times spent waiting for these devices. | Speeding it up involves finding ways to do more computations in the same amount of time. |