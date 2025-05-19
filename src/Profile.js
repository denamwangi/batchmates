import Button from '@mui/material/Button'
import Card from '@mui/material/Card'
import Typography from '@mui/material/Typography'
import CardContent from '@mui/material/CardContent'
import { Box } from '@mui/material'

// {
//     "name": "Emily",
//     "role_and_institution": "Technical Facilitator at Recurse Center",
//     "technical_skills_and_interests": [
//       "Cryptography",
//       "Word games",
//       "Puzzles"
//     ],
//     "goals": [
//       "Run the retreat",
//       "Support participants' technical growth"
//     ],
//     "location": "",
//     "non_technical_hobbies_and_interest": [
//       "Singing",
//       "Music theatre"
//     ],
//     "other": [
//       "Former engineering manager",
//       "Alum (Winter 2 batch)",
//       "Organizer of the RC Crosswording Conclave",
//       "Available for chats via Calendly and Zulip"
//     ]
//   }
export default function Profile(props) {
    const { data } = props;
    const { name, other, role_and_institution,  goals, non_technical_hobbies_and_interest, technical_skills_and_interests} = data;
    return (
      <Box
        sx={{
          width: 300,
          height: 400,
          borderRadius: 1
        }}
      >
        <Card>
          <CardContent>
            <Typography variant="h5">{name}</Typography>
            <Typography variant="body3">{role_and_institution}</Typography>

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