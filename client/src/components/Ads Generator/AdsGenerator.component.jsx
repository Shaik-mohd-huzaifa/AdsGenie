import { useEffect, useState } from 'react';
import './AdsGenerator.styles.scss';
import { LuSettings2 } from "react-icons/lu";
import { SiCodemagic } from "react-icons/si";
import { Parameters } from '../Parameters/parameters.component';
import { useDispatch, useSelector } from 'react-redux';
import { ParameterToggleSelector } from '../../store/Parameters/Parameters.selector';
import { UPDATE_PARAMETER_TOOGLE } from '../../store/Parameters/Parameters.actions';




export const AdsGenerator = () => {
    const ParameterToggle = useSelector(ParameterToggleSelector)
    const dispatch = useDispatch();
    const [ParametersToggle, setParametersToggle] = useState(ParameterToggle)

    useEffect(() => {
        setParametersToggle(ParameterToggle)
    }, [ParameterToggle])
    
    function HandleToggle(){
        dispatch(UPDATE_PARAMETER_TOOGLE())
    }

    return (
        <div className="AdsGenerator-container">
            <button className="settings-icon" onClick={HandleToggle}><LuSettings2/></button>
            <div className="header">
         <h1>Ads Generator</h1>
         <p>A powerful AI-driven ad generation tool that creates high-quality advertisements across multiple aspect ratios simultaneously. Perfect for diverse platforms, it ensures visually stunning, brand-consistent designs optimized for every format. Tailor prompts, color schemes, and audience preferences to generate ads quickly and effortlessly, ready for immediate deployment.</p>
         </div>
        {ParametersToggle && <Parameters/>}
        </div>
    )
}