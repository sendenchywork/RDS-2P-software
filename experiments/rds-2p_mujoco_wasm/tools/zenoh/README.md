# Проверка доставки MotorCommands в браузер

Проверено на Ubuntu 26.04 с ROS 2 Lyrical, Python-клиентом eclipse-zenoh 1.10.0, zenoh-bridge-remote-api 1.10.0 и zenoh-ts 1.10.0. Нужен доступный ROS-интерфейс ftservo_ros/msg/MotorCommands. Проверить его можно командой `ros2 interface show ftservo_ros/msg/MotorCommands` после подключения рабочего пространства ROS.

## Подготовка

Из каталога веб-приложения выполните `npm ci` для самого симулятора. Браузерный приёмник собирается отдельно командой `(cd tools/zenoh && npm ci && npm run build)`. Webpack собирает JavaScript и WASM библиотеки Zenoh в dist.

Для адаптера установите `eclipse-zenoh==1.10.0` в Python-окружение с доступом к rclpy и ftservo_ros (например, venv с --system-site-packages для системного Python ROS). Готовая программа zenoh-bridge-remote-api для Linux входит в standalone-архив [релиза 1.10.0](https://github.com/eclipse-zenoh/zenoh-ts/releases/tag/1.10.0).

## Локальный запуск

Откройте терминалы в каталоге веб-приложения. В терминалах 2 и 4 подключите один и тот же ROS overlay через source install/setup.bash своего рабочего пространства и задайте одинаковый ROS_DOMAIN_ID.

1. Запустите Zenoh (укажите путь к распакованному бинарному файлу).

   ```bash
   zenoh-bridge-remote-api --listen tcp/127.0.0.1:7447 --ws-port 127.0.0.1:10000 --no-multicast-scouting
   ```

2. Запустите ROS-подписчика из Python-окружения с eclipse-zenoh.

   ```bash
   python3 tools/zenoh/bridge.py
   ```

3. Запустите веб-сервер.

   ```bash
   python3 tools/serve.py --host 127.0.0.1 --port 8080
   ```

   Откройте http://127.0.0.1:8080/?zenoh и консоль разработчика. Дождитесь строки `[RDS2P] Listening on rds2p/sim/motors/commands`.

4. Опубликуйте одну команду.

   ```bash
   ros2 topic pub --once -w 1 /motors/commands ftservo_ros/msg/MotorCommands '{commands: [{motor_id: 1, target_position: 0.2}]}'
   ```

В консоли появится строка `[RDS2P] MotorCommands` с массивом commands. Положение указано в радианах двигателя. Адаптер сохраняет заголовок, порядок команд и все поля, отклоняет NaN и бесконечные числа. Браузер выводит полученные данные. Этот этап проверяет только доставку. После перезапуска Zenoh перезагрузите страницу и дождитесь подписки перед отправкой.
