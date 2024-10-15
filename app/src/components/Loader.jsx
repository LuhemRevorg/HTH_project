import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ParticlesComponent from './particles';
import LoaderGIF from "../images/loaderGIF.gif";
import styles from './loader.module.css'; // External CSS file for styling

function Loader() {
  const navigate = useNavigate();

  useEffect(() => {
    // Set a timeout for 5 seconds to transition to the result page
    const timer = setTimeout(() => {
      navigate('/result'); // Redirect to the result page after 5 seconds
    }, 5000);

    // Cleanup the timer when the component unmounts
    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className={styles.loader_container}>
      {/* Blurred background particles */}
      <div className={styles.particles_background}>
        <ParticlesComponent id="particles" />
      </div>

      {/* Loader GIF on top of the particles */}
      <div className={styles.loader_gif}>
        <img src={LoaderGIF} alt="Loading..." />
      </div>
    </div>
  );
}

export default Loader;
