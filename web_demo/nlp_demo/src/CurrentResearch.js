import './_current-research.scss';
import './index.scss';

import { useState, useEffect } from 'react';


import Card from 'react-bootstrap/Card';
import Col from 'react-bootstrap/Col';
import Slider from "react-slick";

import { getJSONData, LoadObject } from './Utilities';

function CurrentResearch (){
    
    
    
    const [researchData, setResearchData] = useState([]);
    
    useEffect( () => {
        const workingDirectory = process.env.PUBLIC_URL + "/data/current_research/";
        const currentResearchTitlesURL =  workingDirectory + "research_list.json";

        async function getResearchData(researchTitles){

            async function getWebpageData(researchTitle){
                return await getJSONData(workingDirectory + researchTitle + "/webpage.json");
            }

            const webpages = await Promise.all(researchTitles.map(getWebpageData));
            const tempResearchData = [];
            for (let index in researchTitles){
                const researchTitle = researchTitles[index];
                const webpage = webpages[index]["webpage"];
                const imageURL =  workingDirectory + researchTitle + "/image.png";
                tempResearchData.push({'title': researchTitle, 
                                       'webpage': webpage, 
                                       'imageURL': imageURL});
            }
            return tempResearchData;
        }
        
        let didCancel = false;
        
        getJSONData(currentResearchTitlesURL)
        .then(getResearchData)
        .then((value) => 
        {
            if(!didCancel){
                setResearchData(value)
            }
        })

        return( () => {didCancel = true;} )
    }, [])

    const slideShow = () => {
        

        const researchSlides = [];
        for (let data of researchData){
            
            const title = data.title;
            const webpage = data.webpage;
            const imageURL = data.imageURL;
            researchSlides.push(
                    <Col key={title}>
                        <a id="current-research-slider" href={webpage} >
                            
                            <Card>
                                <Card.Img variant="top"  src={imageURL} alt="" 
                                          width="300" />
                                <Card.Body>
                                    <Card.Title>
                                        {title}
                                    </Card.Title>
                                </Card.Body>
                            </Card>
                            
                        </a>
                    </Col>
            );
        }
        const settings = {
            dots: true,
            infinite: true,
            speed: 500,
            slidesToScroll: 1,
            slidesToShow: 3,
            autoplay: true,
            autoplaySpeed: 4000,
            responsive: [
                {
                  breakpoint: 1500,
                  settings: {
                    slidesToShow: 2,
                  }
                },
                {
                  breakpoint: 1000,
                  settings: {
                    slidesToShow: 1,
                  }
                }
              ]
          };
        
        return(
            <Slider {...settings}>
                {researchSlides}
            </Slider>
        )
    };

    return(

        <div className="extra-height-padding alternative-color current-research-div" 
             id="full-width">
            <Col xs={12} xl={{span: 8, offset: 2}} >
                <h1>Current Research</h1>
                <hr/>
            </Col>
            <LoadObject data={researchData} onSuccess={slideShow}/>
        </div>
    )
}

export default CurrentResearch;