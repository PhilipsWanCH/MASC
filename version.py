# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 打印python版本1
    import sys
    print_hi('PyCharm')
    import torch
    print("Pytorch version：")
    print(torch.__version__)
    print("CUDA Version: ")
    print(torch.version.cuda)
    print("cuDNN version is :")
    print(torch.backends.cudnn.version())
'''
高级远程拷贝文件方法：

上面直接scp文件夹的方法，如果小文件多，那么scp速度会非常缓慢。可以使用以下方法拷贝。

在北京A区的实例1终端中执行：

cd /root/autodl-tmp/ &&  tar cf - * | ssh -p 66666 root@region-3.autodl.com "cd /root/autodl-tmp && tar xf -"
以上命令可以将实例1中的/root/autodl-tmp目录下所有文件，拷贝到实例2中
'''

# ssh -p 40149 root@region-46.seetacloud.com
# tjJYzVvFQv4r

'''
SSH隧道的方法¶
在实例中启动visdom（默认会监听8097端口）
在本地电脑的终端中执行命令：ssh -CNgv -L 8097:127.0.0.1:8097 root@region-1.autodl.com -p 37881。
其中8097:127.0.0.1:8097是指代理Visdom Server的8097端口到本地的8097端口，
root@region-1.autodl.com和37881分别是实例中SSH指令的访问地址与端口，请进行相应替换。
在本地浏览器中访问127.0.0.1:8097即可打开Visdom
'''

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
