import Card from '@mui/material/Card'
import { Typography } from '@mui/material'
import { CardContent } from '@mui/material'
import { Box } from '@mui/material'

export default function Profile(props) {
    const { data } = props;
    const { name, other, role_and_institution,  goals, non_technical_hobbies_and_interest, technical_skills_and_interests} = data;
    return (
      <Box
        sx={{
          width: 400,
          height: 500,
          borderRadius: 1
        }}
      >
        <Card>
          <CardContent>
            <Typography variant="h5">{name}</Typography>
            <Typography variant="body4">{role_and_institution}</Typography>

            <Typography variant="h6">While at RC:</Typography>
            <Typography variant="body3">{goals.join(', ')}</Typography>


            <Typography variant="h6">Interests:</Typography>
            <Typography variant="body3">{technical_skills_and_interests.join(', ')}</Typography>


            <Typography variant="h6">Hobbies</Typography>
            <Typography variant="body3">{non_technical_hobbies_and_interest.join(', ')}</Typography>

            <Typography variant="h6">Misc</Typography>
            <Typography variant="body3">{other.join(', ')}</Typography>
          </CardContent>
        </Card>
      </Box>
    );
}