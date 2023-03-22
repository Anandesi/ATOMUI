import React, { useState } from 'react';
import axios from 'axios';

function FileUploader() {
  const [response, setResponse] = useState(null);

  const uploadFile = (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
    axios.post('http://localhost:8000/linearregression/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then(response => {
       
      setResponse(response.data);
    })
    .catch(error => {
      console.log(error);
    })
  }

  return (
   

    <div>
      <h1>File Uploader</h1>
      <input type="file" onChange={uploadFile} />
      {/* {response && <img src={response} > result</img>} */}
      {response && 
      <div>
        <img src={`data:image/png;base64,${response.image}`}/>
        <p> slope is: {response.slope} </p>
        <p> intercept is: {response.intercept} </p>
        <p> r_squared is: {response.r_squared} </p>
    </div>
    }
    </div>
    


  );
}

export default FileUploader;
