from fabric import Connection
import os

update_list = ['bin','core','logs','rest_apps','services','tools','utils','main.py','settings.py','__init__.py']


def update():
    with Connection(host='rembern.com', user='root') as con:
        con.connect_kwargs.password='1!P@ssword'
        rm_cm_format = "rm -rf {0}"
        scp_format = "scp -r {0} root@rembern.com:/home/lxl/nlp_server/"
        rm_cm = ";".join([rm_cm_format.format("/home/lxl/nlp_server/" + x) for x in update_list])
        scp_cms = [scp_format.format(x) for x in update_list]
        print(scp_cms)
        result = con.run(rm_cm)
        # result = con.run("cd /home/lxl/kjqb/Recommend/bin;bash /home/lxl/kjqb/Recommend/bin/start.sh restart")
        for scp_cm in scp_cms:
            os.system(scp_cm)
        print(result)


if __name__ == '__main__':
    update()
