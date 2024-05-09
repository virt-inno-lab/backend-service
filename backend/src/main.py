import move_user

bozhinoski = "bozhinoski@yandex.ru"
vova = "vovasst@yandex.ru"
stepan = "tsepa.step@yandex.ru"
i = "sanka.buchnev@ya.ru"

move_user.update_cap(i, move_user.Cap.cloud_auditor)
# ValueError because there is no such user!! woah!!
move_user.update_cap(bozhinoski, move_user.Cap.cloud_auditor)
