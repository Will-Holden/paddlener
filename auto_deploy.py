from fabric import Connection
import os


update_list = [file for file in os.listdir() if not file.startswith(".")]
project_name = "paddleserver"

def update():
    with Connection(host='gpu2', user='weijing') as con:
        con.connect_kwargs.password='weijing'
        rm_cm_format = "rm -rf {0}"
        scp_format = "scp -r {0} lxl@newbee13:/home/lxl/servers/{1}/"
        rm_cm = ";".join([rm_cm_format.format("/home/lxl/servers/" + project_name + "/" + x) for x in update_list])
        scp_cms = [scp_format.format(x, project_name) for x in update_list]
        print(scp_cms)
        result = con.run(rm_cm)
        for scp_cm in scp_cms:
            os.system(scp_cm)
        print(result)


if __name__ == '__main__':
    update()
