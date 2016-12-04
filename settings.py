import os
import json

project_name = "futuretags"

roles = ["superadmin","admin","user"]
apis = [
        {"name":"auth","roles":["all"]},
        {"name":"getCoupons","roles":["admin"]}
       ]

pages = {"superadmin":[                       
                       "brands"
                      ],
         "admin":[
                  "products",
                  "coupons",
                  "myaccount",
                  "geolocation"
                 ],
         "user":[
                  "market",
                  "myaccount"
                ],
         "all":[
                  "home",
                  "howitworks"
               ]
        }


db = {
      "host":"localhost",
      "user":"root",
      "psw":""
     }

media = "/media/"

nginx_path="/etc/nginx/"

