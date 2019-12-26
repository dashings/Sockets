using System;
using System.IO;
using System.Net;
using System.Net.Sockets;

namespace ConsoleApplication2
{
    class Program
    {
        private static byte[] result = new byte[1024];
        static void Main(string[] args)
        {
            Socket receiveSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            IPEndPoint hostIpEndPoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 9998);

            receiveSocket.Bind(hostIpEndPoint);
            //监听
            receiveSocket.Listen(2);
            ////接受客户端连接
            Socket hostSocket = receiveSocket.Accept();

            byte[] buffer = new byte[1000000];
            hostSocket.Receive(buffer, buffer.Length, SocketFlags.None);
            Console.WriteLine("Receive success");

            FileStream fs1 = File.Create("1.jpg");
            fs1.Write(buffer, 0, buffer.Length);
            fs1.Close();


            //关闭接收数据的Socket
            hostSocket.Shutdown(SocketShutdown.Receive);
            hostSocket.Close();
            //关闭发送连接
            receiveSocket.Close();
            
        }
    }
}
