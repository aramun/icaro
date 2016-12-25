import os
import json

project_name = "futuretags"
listen_port = 80
roles = ["superadmin","admin","user"]
default = {"proxy_set_header":["Host $http_host",
                               "X-Real-IP $remote_addr",
                               "X-Forwarded-For $proxy_add_x_forwarded_for",
                               "X-Forwarded-Proto $scheme"
                              ]
          }

apis = [
        {"name":"auth","roles":["all"], "addr":"local", "config_profile": default},
        {"name":"getCoupons","roles":["admin"], "addr":"local", "config_profile": default},
        {"name":"getCoupons","roles":["admin"], "addr":"local", "config_profile": default}
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

#cache_location = "~/"

media = "/media/"

nginx_path="/etc/nginx/"

