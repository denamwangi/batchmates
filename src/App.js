import React, { useState, useEffect } from "react";
import GraphView from "./GraphView";
import Profile from "./Profile";
import { Typography } from "@mui/material";
import { Box } from "@mui/material";
import { Grid } from "@mui/material";

// const response = [

//     {
//       "name": "Emily",
//       "role_and_institution": "Technical Facilitator at Recurse Center",
//       "technical_skills_and_interests": [
//         "Cryptography",
//         "Word games",
//         "Puzzles"
//       ],
//       "goals": [
//         "Run the retreat",
//         "Support participants' technical growth"
//       ],
//       "location": "",
//       "non_technical_hobbies_and_interest": [
//         "Singing",
//         "Music theatre"
//       ],
//       "other": [
//         "Former engineering manager",
//         "Alum (Winter 2 batch)",
//         "Organizer of the RC Crosswording Conclave",
//         "Available for chats via Calendly and Zulip"
//       ]
//     },
//     {
//       "name": "Mike",
//       "role_and_institution": "Former Tech Recruiter and Manager (Etsy, Blue Apron, Datadog), current Recurse Center participant transitioning to SWE",
//       "technical_skills_and_interests": [
//         "coding",
//         "software engineering",
//         "deep dives into new technical topics"
//       ],
//       "goals": [
//         "Go deep on and build around a few topics of interest",
//         "Surround myself with more experienced peers to learn and collaborate"
//       ],
//       "location": "Brooklyn (Red Hook), New York",
//       "non_technical_hobbies_and_interest": [
//         "weightlifting and fitness",
//         "cooking for family",
//         "playing with daughter and exploring city (zoos, aquariums, museums, galleries, parks)",
//         "playing guitar/music",
//         "reading (Warhammer 40k lore)"
//       ],
//       "other": [
//         "Grew up in South Africa, China, and Jordan",
//         "Transitioning career from recruiting into software development"
//       ]
//     }
// ];

function App() {
  const data4 = {
    nodes: [
      { id: "music", type: "interest", val: 3 },
      { id: "puzzles", type: "interest", val: 3 },
      { id: "community engagement", type: "interest", val: 3 },
      { id: "Emily", type: "person" },
      { id: "Robbie", type: "person" },
      { id: "David", type: "person" },
      { id: "Gage", type: "person" },
      { id: "Willem Helmet Pickleman", type: "person" },
      { id: "Aneesh", type: "person" },
      { id: "Huxley", type: "person" },
      { id: "Rachel", type: "person" },
      { id: "Adrien", type: "person" },
      { id: "Raunak", type: "person" },
    ],
    links: [
      { source: "Emily", target: "music" },
      { source: "Emily", target: "puzzles" },
      { source: "David", target: "puzzles" },
      { source: "Robbie", target: "music" },
      { source: "David", target: "music" },
      { source: "Gage", target: "music" },
      { source: "Willem Helmet Pickleman", target: "music" },
      { source: "Aneesh", target: "music" },

      { source: "Emily", target: "community engagement" },
      { source: "David", target: "community engagement" },
      { source: "Huxley", target: "community engagement" },
      { source: "Rachel", target: "community engagement" },
      { source: "Adrien", target: "community engagement" },
      { source: "Raunak", target: "community engagement" },
    ],
  };
  const initialGraphData = data4;
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [graphData, setGraphData] = useState(initialGraphData);
  const handleNodeClick = async (node) => {
    const { id, type } = node;
    console.log("handleNodeClick");
    if (type === "person") {
      const response = await fetch(
        `http://127.0.0.1:8000/person/${id}/interests`
      );
      const response_json = await response.json();
      const interests = response_json["data"]["interests"];
      console.log("response_json['data']", response_json["data"]);
      console.log("interests", interests);
      console.log(graphData);

      // {'id': 'music', 'type': 'interest', val: 3}
      const newNodes = interests.map((interest) => {
        console.log(interest);
        return {
          id: interest,
          type: "interest",
          val: 2,
        };
      });

      const newLinks = interests.map((interest) => ({
        source: id,
        target: interest,
      }));

      console.log("newNodes", newNodes);
      setGraphData((prev) => ({
        links: [...prev.links, ...newLinks],
        nodes: [...prev.nodes, ...newNodes],
      }));
    } else {
    }
  };

  useEffect(() => {}, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/profiles");
        const response_json = await response.json();
        response_json["data"].sort((a, b) => a.name.localeCompare(b.name));
        setData(response_json["data"]);
      } catch (e) {
        console.log(e);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  console.log(graphData);
  return (
    <div className="App">
      <GraphView onNodeClick={handleNodeClick} graphData={graphData} />
      {/* <Box sx={{ flexGrow: 2 }}>
        <Typography variant="h2">BatchMates</Typography>
        {isLoading ? (
          <Typography>Data loading...</Typography>
        ) : (
          
          <Grid container spacing={4}>

          {data.map((profileData) => (
            <Grid size={4}>
              <Profile data={profileData} />
            </Grid>
          ))}
          </Grid>
        )}
      </Box> */}
    </div>
  );
}

export default App;
