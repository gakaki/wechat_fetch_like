using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Fiddler;
using System.IO;
using MongoDB.Bson;
using MongoDB.Driver;

[assembly: Fiddler.RequiredVersion("2.3.5.0")]

namespace FiddlerExtensionWriteLog
{

    public class Violin : IAutoTamper    // Ensure class is public, or Fiddler won't see it!
    {
        StreamWriter w = File.AppendText("log.txt");

        public void Log(string logMessage, TextWriter w)
        {
            w.Write("\r\nLog Entry : ");
            w.WriteLine("{0} {1}", DateTime.Now.ToLongTimeString(),
                DateTime.Now.ToLongDateString());
            w.WriteLine("  :");
            w.WriteLine("  :{0}", logMessage);
            w.WriteLine("-------------------------------");
        }


        public Violin()
        {
      
        }

        public void OnLoad()
        {
            /*   var oPage = new TabPage("Timeline");
                oPage.ImageIndex = (int)Fiddler.SessionIcons.Timeline;
                oView = new TimelineView();
                oPage.Controls.Add(oView);
                oView.Dock = DockStyle.Fill;
                FiddlerApplication.UI.tabsViews.TabPages.Add(oPage);*/
        }
        public void OnBeforeUnload() { }

        public void AutoTamperRequestBefore(Session oSession)
        {
        }
        public void AutoTamperRequestAfter(Session oSession) { }
        public void AutoTamperResponseBefore(Session oSession) { }




        public void AutoTamperResponseAfter(Session oSession)
        {
            MongoClient client  = new MongoClient("mongodb://127.0.0.1:27017");
            var database        = client.GetDatabase("wechat_tmp");
            var coll_tmp        = database.GetCollection<BsonDocument>("tmp");
            var host            = oSession.host;
            var full_url        = oSession.fullUrl;
            var d               = new BsonDocument
            {
                {"url", full_url },
                {"req", oSession.GetRequestBodyAsString()},//这里能存dict的话就更好了
                {"resp", oSession.GetResponseBodyAsString()},//这里能把json解析了是更好了自然
            };

            if ( host.Contains("mp.weixin.qq.com") )
            {
                if (full_url.Contains("/s?src="))
                {
                    d["type"] = "origin";
                    coll_tmp.InsertOne(d);
                }

                if (full_url.Contains("/s?__biz"))
                {
                    d["type"] = "webview";
                    coll_tmp.InsertOne(d);
                }
                if (full_url.Contains("/mp/appmsgreport"))
                {
                    d["type"] = "report";
                    coll_tmp.InsertOne(d);
                }
                if (full_url.Contains("/mp/getappmsgext"))
                {
                    d["type"] = "like";
                    coll_tmp.InsertOne(d);
                }
                if (full_url.Contains("/mp/appmsg_comment?"))
                {
                    d["type"] = "comment";
                    coll_tmp.InsertOne(d);
                }
            }
            

        }

        public void OnBeforeReturningError(Session oSession) { }
    }
}