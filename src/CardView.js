import { Box, Grid, Typography } from "@mui/material";
import Profile from "./Profile";

export default function CardView(props) {
  const { isLoading, data, onProfileButtonClick } = props;
  return (
    <Box sx={{ flexGrow: 2 }}>
      <Typography variant="h2">BatchMates</Typography>
      {isLoading ? (
        <Typography>Data loading...</Typography>
      ) : (
        <Grid container spacing={4} alignItems="stretch">
          {data.map((profileData, idx) => (
            <Grid key={idx} xs={12} sm={6} md={4} item>
              <Profile
                data={profileData}
                onProfileButtonClick={onProfileButtonClick}
              />
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
}
