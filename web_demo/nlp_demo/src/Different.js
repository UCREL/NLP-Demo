//import { useState, useEffect } from 'react';

import TitleContainer  from './TitleContainer'
import LanguageIdentification from './LanguageIdentification';
import SemanticTagging from './SemanticTagging';
import WordCloud from './WordCloud';
import CurrentResearch from './CurrentResearch';
import Contact from './Contact';



const Different = () => {

    //const [lastYPosition, setLastYPosition] = useState(0);
    //const [lastCalled, setLastCalled] = useState(new Date().getTime())

    /*const another = () => {
        const currentTime = new Date().getTime();
        if ((currentTime - lastCalled) > 200){
            setLastCalled(currentTime);
            const currentYPosition = window.scrollY; 
            if (lastYPosition < 2){
                console.log('hello');
                console.log(lastYPosition);
                console.log(currentYPosition);
                setLastYPosition(currentYPosition);
                window.location.hash = '#ab';
            }
        }
        
        
        
        
    }

    useEffect( () => {
        window.addEventListener('scroll', another);
    });*/

    return (
        <div>
            <TitleContainer />
            <LanguageIdentification inFocus={true} />
            <SemanticTagging />
            <WordCloud />
            <CurrentResearch />
            <Contact />
        </div>
    )
}
export default Different