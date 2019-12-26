using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;


namespace Client
{
    class Program
    {
        private static byte[] result = new byte[1024];
        static void Main(string[] args)
        {
            //设定服务器IP地址 
            IPAddress ip = IPAddress.Parse("127.0.0.1");
            Socket clientSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            try
            {
                clientSocket.Connect(new IPEndPoint(ip, 9998)); //配置服务器IP与端口 
                Console.WriteLine("连接服务器成功");
            }
            catch
            {
                Console.WriteLine("连接服务器失败，请按回车键退出！");
                return;
            }
            //通过clientSocket接收数据 
            int receiveLength = clientSocket.Receive(result);
            Console.WriteLine("接收服务器消息：{0}", Encoding.ASCII.GetString(result, 0, receiveLength));
            //通过 clientSocket 发送数据 
            for (int i = 0; i < 10; i++)
            {
                try
                {
                    Thread.Sleep(1000);  //等待1秒钟 
                    string sendMessage = "client send Message Hellp" + DateTime.Now;
                    clientSocket.Send(Encoding.ASCII.GetBytes(sendMessage));
                    Console.WriteLine("向服务器发送消息：{0}" + sendMessage);
                    
                    //发送图片
                    //System.IO.FileStream fs = new System.IO.FileStream(@"F:/Temp/Client/flash01.jpg", System.IO.FileMode.OpenOrCreate, System.IO.FileAccess.Read);
                    //byte[] fssize = new byte[fs.Length];
                    //System.IO.BinaryReader strread = new System.IO.BinaryReader(fs);
                    //strread.Read(fssize, 0, fssize.Length - 1);
                    //sendsocket.Send(fssize);
                    //fs.Close();
                    
                }
                catch
                {
                    clientSocket.Shutdown(SocketShutdown.Both);
                    clientSocket.Close();
                    break;
                }
            }
            Console.WriteLine("发送完毕，按回车键退出");
            Console.ReadLine();
        }
    }
}
