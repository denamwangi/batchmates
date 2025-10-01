import React from "react";
import Card from "@mui/material/Card";
import { Typography } from "@mui/material";
import { CardContent } from "@mui/material";
import { Box, Button, Link } from "@mui/material";

export default function Profile(props) {
  const { data, onProfileButtonClick } = props;
  const {
    name,
    other,
    role_and_institution,
    goals,
    non_technical_hobbies_and_interest,
    technical_skills_and_interests,
  } = data;

  const addLinkToInterest = (interest) => {
    const href = `/graph?interest=${interest}`;
    return <Link href={href}>{interest}</Link>;
  };

  return (
    <Box
      sx={{
        width: 400,
        height: 600,
        borderRadius: 1,
      }}
    >
      <Card sx={{ height: "100%", display: "flex", flexDirection: "column" }}>
        <CardContent sx={{ overflow: "auto", flexGrow: 1 }}>
          <Typography variant="h5">{name}</Typography>
          <Typography variant="body4">{role_and_institution}</Typography>

          <Typography variant="h6">While at RC:</Typography>
          <Typography variant="body3">{goals.join(", ")}</Typography>

          <Typography variant="h6">Interests:</Typography>
          {technical_skills_and_interests.map((interest, index) => (
            <React.Fragment key={`tech-${index}`}>
              {addLinkToInterest(interest)}
              {index < technical_skills_and_interests.length - 1 && (
                <Typography component="span">, </Typography>
              )}
            </React.Fragment>
          ))}

          <Typography variant="h6">Hobbies</Typography>
          <Typography variant="body3">
            {non_technical_hobbies_and_interest.map((interest, index) => (
              <React.Fragment key={`hobby-${index}`}>
                {addLinkToInterest(interest)}
                {index < non_technical_hobbies_and_interest.length - 1 && (
                  <Typography component="span">, </Typography>
                )}
              </React.Fragment>
            ))}
          </Typography>

          <Typography variant="h6">Misc</Typography>
          <Typography variant="body3">{other.join(", ")}</Typography>

          {/* <Button onClick={() => onProfileButtonClick(data)}>See Viz</Button> */}
        </CardContent>
      </Card>
    </Box>
  );
}
