import React from 'react'
import ReactDOM from 'react-dom'
import App from './App'

import 'bootstrap-icons/font/bootstrap-icons.css'
import './index.scss'


const rootElement = document.getElementById("root");

if (rootElement.hasChildNodes()) {
  ReactDOM.hydrate(<App />, rootElement);
} else {
  ReactDOM.render(<App />, rootElement);
}

//ReactDOM.render(<App />, document.getElementById('root'))