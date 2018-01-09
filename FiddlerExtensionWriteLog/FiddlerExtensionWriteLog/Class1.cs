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
            if (oSession.fullUrl.Contains("getappmsgext"))
            {
                MongoClient client = new MongoClient("mongodb://127.0.0.1:27017");

                //var d = new Dictionary<string,string>
                var d = new BsonDocument
                {
                    {"url", oSession.fullUrl },
                    {"req", oSession.GetRequestBodyAsString()},
                    {"resp", oSession.GetResponseBodyAsString()},
                    
                };
                //write mongodb 


                var database = client.GetDatabase("xcar");
                var collection = database.GetCollection<BsonDocument>("like_nums");
                collection.InsertOne(d);
            }

               

            
           
        }

        public void OnBeforeReturningError(Session oSession) { }
    }
}