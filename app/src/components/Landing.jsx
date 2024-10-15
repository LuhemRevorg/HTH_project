import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './landing.module.css';
import BackgroundVideo from '../videos/background-video.mp4'; 

const sentences = [
  "Revolutionalize the world",
  "Make each move with confidence",
  "Reach the hearts of people",
  "Boost your confidence",
  "Train your inner speaker",
  "Master Vocal projection"
];

function Landing() {
  const [currentSentenceIndex, setCurrentSentenceIndex] = useState(0);
  const [isTextVisible, setIsTextVisible] = useState(false);
  const [isBlurred, setIsBlurred] = useState(false);
  const [showSpeakerBoxes, setShowSpeakerBoxes] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const timerBlur = setTimeout(() => {
      setIsBlurred(true);
      setIsTextVisible(true);
    }, 3000);

    const textCycleInterval = setInterval(() => {
      setCurrentSentenceIndex((prevIndex) => (prevIndex + 1) % sentences.length);
    }, 3000);

    const speakerTimer = setTimeout(() => {
      setShowSpeakerBoxes(true);
    }, 3500);

    return () => {
      clearTimeout(timerBlur);
      clearTimeout(speakerTimer);
      clearInterval(textCycleInterval);
    };
  }, []);

  const getStyledSentence = (sentence) => {
    const words = sentence.split(' ');
    return (
      <>
        <span className={styles.purple_word}>{words[0]}</span> {words.slice(1).join(' ')}
      </>
    );
  };

  return (
    <div className={styles.landing_page}>
      <video
        autoPlay
        muted
        loop
        className={`${styles.background_video} ${isBlurred ? styles.blur_effect : ''}`}
      >
        <source src={BackgroundVideo} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      
      <div className={`${styles.speaker_container} ${showSpeakerBoxes ? styles.show : ''}`}>
        <button className={styles.speaker_button} onClick={() => navigate('/main')}>Get Started</button>
      </div>
    </div>
  );
}

export default Landing;
