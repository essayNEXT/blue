# blue
<h1> Важно !!!</h1>
Столкнулись с проблемой связаной с символоми окончания строки. 
<a href="https://docs.github.com/ru/get-started/getting-started-with-git/configuring-git-to-handle-line-endings"> Описание на Git </a>

Решается следующими образом:
1. Сохранить все изменения (коммит) 
2. git config --global core.autocrlf input
3. git rm --cached -r .
4. git reset --hard
5. Перезагрузить проект из репозитория

<h2> Команды для контейнера Django</h2>

После запуска контейнера Django, необходимо прописать в командной строке контейнера:
1. python manage.py migrate (сделать миграции)
2. python manage.py createsuperuser (создать админа)
3. python manage.py collectstatic (подключить статику)

Это нужно делать при первом запуске и после каждого удаления томов.

