import React from "react";
import GraphView from "./GraphView";
import Profile from "./Profile";
import { Typography } from "@mui/material";
 import { Box } from "@mui/material";
import { Grid } from '@mui/material'


const response = [

    {
      "name": "Emily",
      "role_and_institution": "Technical Facilitator at Recurse Center",
      "technical_skills_and_interests": [
        "Cryptography",
        "Word games",
        "Puzzles"
      ],
      "goals": [
        "Run the retreat",
        "Support participants' technical growth"
      ],
      "location": "",
      "non_technical_hobbies_and_interest": [
        "Singing",
        "Music theatre"
      ],
      "other": [
        "Former engineering manager",
        "Alum (Winter 2 batch)",
        "Organizer of the RC Crosswording Conclave",
        "Available for chats via Calendly and Zulip"
      ]
    },
    {
      "name": "Mike",
      "role_and_institution": "Former Tech Recruiter and Manager (Etsy, Blue Apron, Datadog), current Recurse Center participant transitioning to SWE",
      "technical_skills_and_interests": [
        "coding",
        "software engineering",
        "deep dives into new technical topics"
      ],
      "goals": [
        "Go deep on and build around a few topics of interest",
        "Surround myself with more experienced peers to learn and collaborate"
      ],
      "location": "Brooklyn (Red Hook), New York",
      "non_technical_hobbies_and_interest": [
        "weightlifting and fitness",
        "cooking for family",
        "playing with daughter and exploring city (zoos, aquariums, museums, galleries, parks)",
        "playing guitar/music",
        "reading (Warhammer 40k lore)"
      ],
      "other": [
        "Grew up in South Africa, China, and Jordan",
        "Transitioning career from recruiting into software development"
      ]
    }
];

function App() {

  return (
    <div className="App">
      {/* <GraphView /> */}
      <Box sx={{ flexGrow: 1 }}>
        <Typography variant="h2">BatchMates</Typography>
        <Grid container spacing={4}>

          <Grid size={4}>
            <Profile data={response[0]} />
          </Grid>
          <Grid size={4}>
            <Profile data={response[1]} />
          </Grid>
          <Grid size={4}>
            <Profile data={response[0]} />
          </Grid>
          <Grid size={4}>
            <Profile data={response[1]} />
          </Grid>
        </Grid>
      </Box>
    </div>
  );
}

export default App;
