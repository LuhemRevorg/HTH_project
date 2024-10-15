import React, { useEffect, useState, useRef } from 'react';
import ParticlesComponent from './particles2';
import styles from "./result.module.css";
import Papa from 'papaparse';  // Import PapaParse

function Result() {
  const [comments, setComments] = useState([]); // State to hold comments
  const [script, setScript] = useState('');
  const [csvPace, setCsvPace] = useState([]); // State to hold parsed CSV data
  const [audioUrl, setAudioUrl] = useState(''); // State to hold audio URL
  const [summary, setSummary] = useState(''); // State to hold the summary of speech pace
  const audioRef = useRef(null); // Reference to the audio element
  const [isPlaying, setIsPlaying] = useState(false); // State to manage playback
  const [stutter, setStutter] = useState('');
  //const [misspell, setMisspell] = useState('');
  const [pitchCSV, setPitchCSV] = useState([]);

  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await fetch('http://localhost:8080/get-comments');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setComments(data.comments);
        setScript(data.script);
        setStutter(data.stutter);
        setAudioUrl(data.audio);
        //setMisspell(data.misspoken_feedback);
        setPitchCSV(data.pitch_deviations);
        
        if (data.pace_csv) {
          Papa.parse(data.pace_csv, {
            header: true,
            complete: (results) => {
              setCsvPace(results.data); // Store parsed CSV data
              console.log("Parsed CSV Data:", results.data); // Log parsed data
              analyzePace(results.data); // Analyze the parsed data
            },
            error: (error) => {
              console.error("Error parsing CSV:", error);
            }
          });
        }
      } catch (error) {
        console.error('Error fetching comments:', error);
      }
    };

    fetchComments();
  }, []);

  // Analyze speech pace data
  const analyzePace = (data) => {
    const paceSummary = [];
    const paceCounts = { very_slow: 0, medium_slow: 0, medium_fast: 0, very_fast: 0 };

    for (let i = 0; i < data.length - 1; i++) {
      const { start_time, speech_pace } = data[i];
      paceSummary.push(`From ${start_time}s, you were "${speech_pace}".`);
      
      // Count occurrences of each pace
      if (speech_pace in paceCounts) {
        paceCounts[speech_pace]++;
      }
    }

    // Determine overall sentiment
    const majority = Object.keys(paceCounts).reduce((a, b) => paceCounts[a] > paceCounts[b] ? a : b);

    let overallComment;
    if (paceCounts.very_slow > Math.max(paceCounts.medium_slow, paceCounts.medium_fast, paceCounts.very_fast)) {
      overallComment = "It's important to work on maintaining a steady pace.";
    } else if (paceCounts.medium_slow > Math.max(paceCounts.very_slow, paceCounts.medium_fast, paceCounts.very_fast)) {
      overallComment = "Good job! You maintained a medium slow pace.";
    } else {
      overallComment = "Great job! You were quick and articulate.";
    }

    setSummary(`${paceSummary.join(' ')} ${overallComment}`);
  };

  // Function to calculate dot position based on timestamp
  const calculateDotPosition = (timestamp) => {
    const totalDuration = 60; // Adjust this based on the total length of your recording in seconds
    const [minutes, seconds] = timestamp.split(':').map(Number);
    return ((minutes * 60 + seconds) / totalDuration) * 100; // Percentage position
  };

  const handlePlayButtonClick = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  return (
    <div className={styles.mainBody}>
      <ParticlesComponent id="particles" />
      <div className={styles.comments_section}>
        <div className={styles.ai_analysis_box}>
          <h2>AI Analysis</h2>
          {/* <button onClick={() => textToSpeech(script)}>Hear AI</button> */}

          {/* Displaying the Summary Paragraph */}
        </div>
        <div className={styles.scrollBox}>
          <h2>Data:</h2>
  
          <div>
            Your transcript:
          </div>
          <h3>{script}</h3>
          <div className={styles.summaryContainer}>
            <div className={styles.summaryBox}>
              <label>Pace summary:</label>
              <p>{summary}</p>
            </div>
            <div className={styles.summaryBox}>
              <label>Stuttering summary:</label>
              <p>{stutter}</p>
            </div>
            <div className={styles.summaryBox}>
              <label>Misspoken words summary:</label>
              <p>No mispoken words! Going great :)</p>
            </div>
            <div className={styles.summaryBox}>
              <label>These are words where you should emphasize:</label>
               {/* Pitch CSV Table */}
        <div className={styles.pitchTable}>
          <h2>Pitch Data</h2>
          <table>
            <thead>
              <tr>
                <th>Loudness</th>
                <th>Timestamp:</th>
                <th>Word</th>
              </tr>
            </thead>
            <tbody>
                    {pitchCSV.map((item, index) => (
                      <tr key={index}>
                        <td>{item.Deviation}</td>
                        <td>{item.Start}</td>
                        <td>{item.Word}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        <audio ref={audioRef} src={audioUrl} preload="auto" /> {/* Include audio element */}
      </div>
    </div>
  );
}

export default Result;
