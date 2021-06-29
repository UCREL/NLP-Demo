import './index.scss'

import { useState } from 'react';

import Jumbotron from 'react-bootstrap/Jumbotron';
import Col from 'react-bootstrap/Col';

import {ReactComponent as QRCode} from './images/qr-code.svg';
import {ReactComponent as LULogo} from './images/lu-logo.svg';
import {ReactComponent as UCRELLogo} from './images/ucrel-logo.svg';


const showQRCode = (

    <div id="qr-code-div">
            <div className="text-center p-1 flex flex-center items-stretch">
                    <h1 className="pr-3 mb-0" style={{"alignSelf": "center"}}>
                        QR code to this website:
                    </h1>
                    <svg   viewBox="0 0 1160 1160" preserveAspectRatio="xMidYMid meet">
                        <QRCode height="100%"/>
                    </svg>
            </div>
    </div>
)



const TitleContainer = () => {

    const [toggleQR, setToggleQR] = useState(false);

    let qrDiv = ""
    
    if (toggleQR){
        qrDiv = showQRCode;
    }

    return (
        <Jumbotron id="title-div">
            <header>
                <div>
                    <LULogo height="100%"/>
                    <svg id="svg-pointer" viewBox="0 0 290 283.25" height="100%" x="0px" y="0px" 
                         preserveAspectRatio="xMidYMid meet" onClick={()=>{setToggleQR(!toggleQR);}}>
                                <UCRELLogo/>
                    </svg>
                </div>
            </header>

            <div id="image-background" >

            </div>
            <div id="title-text-div" >
                
                <Col md={12} lg={{span: 8, offset: 2}} className="text-center">
                    <h1 className="display-1">What is Natural Language Processing?</h1>
                    <blockquote className="lead">
                        <p className="lead">
                            It is a field of designing methods and algorithms that take 
                            as input or produce as output unstructured, natural language data.
                        </p>
                        <footer><i className="bi bi-dash" role="img" aria-label="Dash"/>
                            <cite>
                                <a href="https://doi.org/10.2200/S00762ED1V01Y201703HLT037">
                                Neural Network Methods for Natural Language 
                                Processing</a> by Yoav Goldberg
                            </cite>
                        </footer>
                </blockquote>
                </Col>
            </div>
            {qrDiv}
            


            
            
        </Jumbotron>
    )
}

export default TitleContainer