import React from 'react'
import ReactDom from 'react-dom'

import $ from 'jquery';

class User extends React.Component {
  componentDidMount() {
      localStorage.setItem("QuesNumber",0);
      //--------Getting token-----------------
         $.ajax({
          url: 'https://mananxunbao.herokuapp.com/api/token/',
          type: "POST",
          crossDomain : true,
          dataType: 'json',
          data: JSON.stringify( {
              username: 'sanyam',
              password: 's2ny2mmitt2l'
            }),
          contentType: "application/json",
          success: function (data) {
            
              var tokenvalue = data.access;
              console.log(tokenvalue);
              localStorage.setItem("token",tokenvalue);
             
              
          },
          error: function () {
          	
          localStorage.clear();
       
      }
  })
      //--------Posting Fb Details-----------------
      
      $.ajax({
          url: 'https://mananxunbao.herokuapp.com/api/userprofile/',
          type: "POST",
          crossDomain : true,
          dataType: 'json',
           headers: {
              "Authorization":"Bearer " + localStorage.getItem("token")
            },
          data: JSON.stringify( {
              name:localStorage.getItem("fullname"),
              pic:localStorage.getItem("userimg"),
              fid:localStorage.getItem("facebookid")
            }),
          contentType: "application/json",
          success: function () {
            
              
             console.log("success posting");
              
          }
  })
    
      
      //--------User Details-----------------
      
            $("#user_text").append(localStorage.getItem("fullname"));
            $("#user_image").attr("src", localStorage.getItem("userimg"));

        }

      
    render() {
    return (
    
     <div className = "user" >
        
        <img src={""} alt id="user_image" />
        </div>
        
 
   
     
    );}
}


export default User;