import { useState } from "react";
import { 
  Briefcase, Sparkles, MapPin, Building2, User, ExternalLink, Search, Filter
} from "lucide-react";
import { Badge } from "@/components/ui/badge";

const statusConfig: Record<string, { label: string; className: string }> = {
  new: { label: "New", className: "bg-primary/15 text-primary border-primary/30" },
  applied: { label: "Applied", className: "bg-success/15 text-success border-success/30" },
  tailoring: { label: "Tailoring", className: "bg-warning/15 text-warning border-warning/30" },
  failed: { label: "Failed", className: "bg-destructive/15 text-destructive border-destructive/30" },
};

const jobs = [
  {
    "id": "1",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Madhu Joshi",
    "status": "new",
    "posted": "{'timestamp': 1775224261647, 'date': '2026-04-03T13:51:01.647Z', 'postedAgoShort': '14h', 'postedAgoText': '14 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "2",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Melanie Mehra",
    "status": "new",
    "posted": "{'timestamp': 1773843046985, 'date': '2026-03-18T14:10:46.985Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "3",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Dane Dan",
    "status": "new",
    "posted": "{'timestamp': 1774944361022, 'date': '2026-03-31T08:06:01.022Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "4",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Akanksha Mengi",
    "status": "new",
    "posted": "{'timestamp': 1774946642700, 'date': '2026-03-31T08:44:02.700Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "5",
    "title": "SAP Specialist",
    "company": "Pacer Group",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Pallabi Pal",
    "status": "new",
    "posted": "{'timestamp': 1775136101288, 'date': '2026-04-02T13:21:41.288Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "6",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "LAXMIKANTH PATIL",
    "status": "new",
    "posted": "{'timestamp': 1775196761066, 'date': '2026-04-03T06:12:41.066Z', 'postedAgoShort': '21h', 'postedAgoText': '21 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "7",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jennifer Sosa Eskenazi",
    "status": "new",
    "posted": "{'timestamp': 1773833181248, 'date': '2026-03-18T11:26:21.248Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "8",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sonali More",
    "status": "new",
    "posted": "{'timestamp': 1775042677629, 'date': '2026-04-01T11:24:37.629Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "9",
    "title": "SAP Specialist",
    "company": "Tata Technologies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ranjeeta. Sarkar",
    "status": "new",
    "posted": "{'timestamp': 1775127643329, 'date': '2026-04-02T11:00:43.329Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "10",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nitin Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1774712774439, 'date': '2026-03-28T15:46:14.439Z', 'postedAgoShort': '6d', 'postedAgoText': '6 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "11",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Hemant Rawat",
    "status": "new",
    "posted": "{'timestamp': 1773345136314, 'date': '2026-03-12T19:52:16.314Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "12",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ram K.",
    "status": "new",
    "posted": "{'timestamp': 1775221175600, 'date': '2026-04-03T12:59:35.600Z', 'postedAgoShort': '14h', 'postedAgoText': '14 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "13",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Muskan Singh",
    "status": "new",
    "posted": "{'timestamp': 1775231736003, 'date': '2026-04-03T15:55:36.003Z', 'postedAgoShort': '11h', 'postedAgoText': '11 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "14",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Karthik Kanaji",
    "status": "new",
    "posted": "{'timestamp': 1775149877441, 'date': '2026-04-02T17:11:17.441Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "15",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sophia (Anu) Singh",
    "status": "new",
    "posted": "{'timestamp': 1773854141553, 'date': '2026-03-18T17:15:41.553Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "16",
    "title": "SAP Specialist",
    "company": "Future Creation Placement Consultancy",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Mayuri Shinde",
    "status": "new",
    "posted": "{'timestamp': 1775105588116, 'date': '2026-04-02T04:53:08.116Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "17",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nitin Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1772985934422, 'date': '2026-03-08T16:05:34.422Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "18",
    "title": "SAP Specialist",
    "company": "Tata Technologies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ranjeeta. Sarkar",
    "status": "new",
    "posted": "{'timestamp': 1775129577843, 'date': '2026-04-02T11:32:57.843Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "19",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Suhayra D.",
    "status": "new",
    "posted": "{'timestamp': 1774960481013, 'date': '2026-03-31T12:34:41.013Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "20",
    "title": "SAP Specialist",
    "company": "3S Business Corporation Inc",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Kasu Varma",
    "status": "new",
    "posted": "{'timestamp': 1775226016993, 'date': '2026-04-03T14:20:16.993Z', 'postedAgoShort': '13h', 'postedAgoText': '13 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "21",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Namrata Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1774011561271, 'date': '2026-03-20T12:59:21.271Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "22",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nitin Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1775063318834, 'date': '2026-04-01T17:08:38.834Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "23",
    "title": "SAP Specialist",
    "company": "PRECISION ENTERPRISE",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Varsha Mavani",
    "status": "new",
    "posted": "{'timestamp': 1773587803123, 'date': '2026-03-15T15:16:43.123Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "24",
    "title": "SAP Specialist",
    "company": "TotalTek | Connecting great people with meaningful SAP oppor",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "April Perez",
    "status": "new",
    "posted": "{'timestamp': 1773154126548, 'date': '2026-03-10T14:48:46.548Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "25",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "BK Pandey",
    "status": "new",
    "posted": "{'timestamp': 1775028344204, 'date': '2026-04-01T07:25:44.204Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "26",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Krishna Sameera V",
    "status": "new",
    "posted": "{'timestamp': 1775024387355, 'date': '2026-04-01T06:19:47.355Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "27",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Daniel Andrews",
    "status": "new",
    "posted": "{'timestamp': 1772727753620, 'date': '2026-03-05T16:22:33.620Z', 'postedAgoShort': '4w', 'postedAgoText': '0 months ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "28",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "VOXE",
    "status": "new",
    "posted": "{'timestamp': 1773052980794, 'date': '2026-03-09T10:43:00.794Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "29",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Yin Pengcheng",
    "status": "new",
    "posted": "{'timestamp': 1774933699246, 'date': '2026-03-31T05:08:19.246Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "30",
    "title": "SAP Specialist",
    "company": "Zentek Infosoft",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Shruti Soni",
    "status": "new",
    "posted": "{'timestamp': 1774937389848, 'date': '2026-03-31T06:09:49.848Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "31",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Timothy Clauws",
    "status": "new",
    "posted": "{'timestamp': 1775050850084, 'date': '2026-04-01T13:40:50.084Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "32",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Trishiv AI Tech Services",
    "status": "new",
    "posted": "{'timestamp': 1775209767950, 'date': '2026-04-03T09:49:27.950Z', 'postedAgoShort': '18h', 'postedAgoText': '18 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "33",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "HAREESH TEJA THOTA",
    "status": "new",
    "posted": "{'timestamp': 1775194219828, 'date': '2026-04-03T05:30:19.828Z', 'postedAgoShort': '22h', 'postedAgoText': '22 hours ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "34",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Hire Soft Solutions",
    "status": "new",
    "posted": "{'timestamp': 1775244651613, 'date': '2026-04-03T19:30:51.613Z', 'postedAgoShort': '8h', 'postedAgoText': '8 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "35",
    "title": "SAP Specialist",
    "company": "CoreVia | Full Cycle Recruitment Strategist | Talent Acquisi",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Munish Thakur",
    "status": "new",
    "posted": "{'timestamp': 1774024225655, 'date': '2026-03-20T16:30:25.655Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "36",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Susmitha Reddy",
    "status": "new",
    "posted": "{'timestamp': 1775222812217, 'date': '2026-04-03T13:26:52.217Z', 'postedAgoShort': '14h', 'postedAgoText': '14 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "37",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Vartika Gupta",
    "status": "new",
    "posted": "{'timestamp': 1775100438381, 'date': '2026-04-02T03:27:18.381Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "38",
    "title": "SAP Specialist",
    "company": "DXC Technology | DACH Region | Recruitment | Sourcing | HR |",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Monika Z.",
    "status": "new",
    "posted": "{'timestamp': 1772725251611, 'date': '2026-03-05T15:40:51.611Z', 'postedAgoShort': '4w', 'postedAgoText': '0 months ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "39",
    "title": "SAP Specialist",
    "company": "Infosys",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sanjana Malik",
    "status": "new",
    "posted": "{'timestamp': 1773288893871, 'date': '2026-03-12T04:14:53.871Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "40",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Everita Blanchette",
    "status": "new",
    "posted": "{'timestamp': 1773298681713, 'date': '2026-03-12T06:58:01.713Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "41",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Yamini Atchuta",
    "status": "new",
    "posted": "{'timestamp': 1775024312481, 'date': '2026-04-01T06:18:32.481Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "42",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Tom Cullen",
    "status": "new",
    "posted": "{'timestamp': 1773337235353, 'date': '2026-03-12T17:40:35.353Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "43",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ajit Deshpande",
    "status": "new",
    "posted": "{'timestamp': 1772831853696, 'date': '2026-03-06T21:17:33.696Z', 'postedAgoShort': '4w', 'postedAgoText': '0 months ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "44",
    "title": "SAP Specialist",
    "company": "BlueRock Resources | \ud83d\udc8eSmarter Hiring in SAP, DATA & AI. Lowe",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Zane Grieve-Fitzell",
    "status": "new",
    "posted": "{'timestamp': 1773674107788, 'date': '2026-03-16T15:15:07.788Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "45",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Dr. Mahesh Kumar C.V.",
    "status": "new",
    "posted": "{'timestamp': 1773284406169, 'date': '2026-03-12T03:00:06.169Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "46",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Atul Kumar Kaushik",
    "status": "new",
    "posted": "{'timestamp': 1775150057480, 'date': '2026-04-02T17:14:17.480Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "47",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Pavani N",
    "status": "new",
    "posted": "{'timestamp': 1775038021268, 'date': '2026-04-01T10:07:01.268Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "48",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Rian Morgan",
    "status": "new",
    "posted": "{'timestamp': 1773740651766, 'date': '2026-03-17T09:44:11.766Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "49",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Krishna swetha",
    "status": "new",
    "posted": "{'timestamp': 1775230269299, 'date': '2026-04-03T15:31:09.299Z', 'postedAgoShort': '12h', 'postedAgoText': '12 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "50",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Djilali FEGHOULI, PMP",
    "status": "new",
    "posted": "{'timestamp': 1773931917743, 'date': '2026-03-19T14:51:57.743Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "51",
    "title": "SAP Specialist",
    "company": "Whitehall Resources",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Emily Brett",
    "status": "new",
    "posted": "{'timestamp': 1773052167185, 'date': '2026-03-09T10:29:27.185Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "52",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Hemanth H",
    "status": "new",
    "posted": "{'timestamp': 1773330786570, 'date': '2026-03-12T15:53:06.570Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "53",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jak Tompsett",
    "status": "new",
    "posted": "{'timestamp': 1775122630659, 'date': '2026-04-02T09:37:10.659Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "54",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Reading jobs, Berkshire",
    "status": "new",
    "posted": "{'timestamp': 1775214827167, 'date': '2026-04-03T11:13:47.167Z', 'postedAgoShort': '16h', 'postedAgoText': '16 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "55",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sana Asher",
    "status": "new",
    "posted": "{'timestamp': 1775048486670, 'date': '2026-04-01T13:01:26.670Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "56",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Lauren Gagliardi",
    "status": "new",
    "posted": "{'timestamp': 1774467902866, 'date': '2026-03-25T19:45:02.866Z', 'postedAgoShort': '1w', 'postedAgoText': '1 week ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "57",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sachin Sharma",
    "status": "new",
    "posted": "{'timestamp': 1773072184043, 'date': '2026-03-09T16:03:04.043Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "58",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Pamela M.",
    "status": "new",
    "posted": "{'timestamp': 1773073143086, 'date': '2026-03-09T16:19:03.086Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "59",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Siva Jyothi (Catherine)",
    "status": "new",
    "posted": "{'timestamp': 1775224172200, 'date': '2026-04-03T13:49:32.200Z', 'postedAgoShort': '14h', 'postedAgoText': '14 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "60",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "SAGE Business Solutions Inc.",
    "status": "new",
    "posted": "{'timestamp': 1775183105553, 'date': '2026-04-03T02:25:05.553Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "61",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sachin Sharma",
    "status": "new",
    "posted": "{'timestamp': 1773075426577, 'date': '2026-03-09T16:57:06.577Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "62",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jan Sirirat",
    "status": "new",
    "posted": "{'timestamp': 1773199925110, 'date': '2026-03-11T03:32:05.110Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "63",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Pallavi G.",
    "status": "new",
    "posted": "{'timestamp': 1773638886151, 'date': '2026-03-16T05:28:06.151Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "64",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Callum George",
    "status": "new",
    "posted": "{'timestamp': 1774936808229, 'date': '2026-03-31T06:00:08.229Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "65",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ajit Deshpande",
    "status": "new",
    "posted": "{'timestamp': 1774842900033, 'date': '2026-03-30T03:55:00.033Z', 'postedAgoShort': '4d', 'postedAgoText': '4 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "66",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sachin Sharma",
    "status": "new",
    "posted": "{'timestamp': 1773674897189, 'date': '2026-03-16T15:28:17.189Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "67",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Luis R. Orecchia",
    "status": "new",
    "posted": "{'timestamp': 1774962967949, 'date': '2026-03-31T13:16:07.949Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "68",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Emma Adams",
    "status": "new",
    "posted": "{'timestamp': 1775032212061, 'date': '2026-04-01T08:30:12.061Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "69",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Wouter van Heddeghem",
    "status": "new",
    "posted": "{'timestamp': 1774974387007, 'date': '2026-03-31T16:26:27.007Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "70",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "MICKAEL QUESNOT",
    "status": "new",
    "posted": "{'timestamp': 1774867148001, 'date': '2026-03-30T10:39:08.001Z', 'postedAgoShort': '4d', 'postedAgoText': '4 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "71",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Fazal N.",
    "status": "new",
    "posted": "{'timestamp': 1775052902353, 'date': '2026-04-01T14:15:02.353Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "72",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "MICKAEL QUESNOT",
    "status": "new",
    "posted": "{'timestamp': 1775131583540, 'date': '2026-04-02T12:06:23.540Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "73",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "ConSAP",
    "status": "new",
    "posted": "{'timestamp': 1775081748616, 'date': '2026-04-01T22:15:48.616Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "74",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Vinay Pasalkar",
    "status": "new",
    "posted": "{'timestamp': 1775136478250, 'date': '2026-04-02T13:27:58.250Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "75",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Fazal N.",
    "status": "new",
    "posted": "{'timestamp': 1775139301599, 'date': '2026-04-02T14:15:01.599Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "76",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sachin Sharma",
    "status": "new",
    "posted": "{'timestamp': 1773677371724, 'date': '2026-03-16T16:09:31.724Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "77",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nik Kaniewski",
    "status": "new",
    "posted": "{'timestamp': 1775233653112, 'date': '2026-04-03T16:27:33.112Z', 'postedAgoShort': '11h', 'postedAgoText': '11 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "78",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Badarinadh Gelli",
    "status": "new",
    "posted": "{'timestamp': 1774931402978, 'date': '2026-03-31T04:30:02.978Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "79",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Daniel Ross",
    "status": "new",
    "posted": "{'timestamp': 1774942208216, 'date': '2026-03-31T07:30:08.216Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "80",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jean Shaw, MHRM",
    "status": "new",
    "posted": "{'timestamp': 1775079962115, 'date': '2026-04-01T21:46:02.115Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "81",
    "title": "SAP Specialist",
    "company": "Scale Project Leadership | SAP | Microsoft | Cloud | FSCP | ",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ivan Snell",
    "status": "new",
    "posted": "{'timestamp': 1775033987347, 'date': '2026-04-01T08:59:47.347Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "82",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Rajdeep Ghosh",
    "status": "new",
    "posted": "{'timestamp': 1775044112531, 'date': '2026-04-01T11:48:32.531Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "83",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Gayathri Saggam",
    "status": "new",
    "posted": "{'timestamp': 1775192532830, 'date': '2026-04-03T05:02:12.830Z', 'postedAgoShort': '22h', 'postedAgoText': '22 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "84",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Bundy Baking Solutions",
    "status": "new",
    "posted": "{'timestamp': 1773930448853, 'date': '2026-03-19T14:27:28.853Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "85",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Bente Grundt Hansen",
    "status": "new",
    "posted": "{'timestamp': 1773662303476, 'date': '2026-03-16T11:58:23.476Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "86",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Cyntia Jones, MPA, PMP, RTE",
    "status": "new",
    "posted": "{'timestamp': 1773860845190, 'date': '2026-03-18T19:07:25.190Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "87",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Amer Ali",
    "status": "new",
    "posted": "{'timestamp': 1774958433854, 'date': '2026-03-31T12:00:33.854Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "88",
    "title": "SAP Specialist",
    "company": "Dexian | Part time Hockey Skills instructor & Coach of the 2",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Colin Clapton",
    "status": "new",
    "posted": "{'timestamp': 1773846312004, 'date': '2026-03-18T15:05:12.004Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "89",
    "title": "SAP Specialist",
    "company": "YASH Technologies | Connecting Top SAP Talent with Exception",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Samiksha Dubey",
    "status": "new",
    "posted": "{'timestamp': 1775116099694, 'date': '2026-04-02T07:48:19.694Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "90",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jorge Batista",
    "status": "new",
    "posted": "{'timestamp': 1775247779403, 'date': '2026-04-03T20:22:59.403Z', 'postedAgoShort': '7h', 'postedAgoText': '7 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "91",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sugam Saurav",
    "status": "new",
    "posted": "{'timestamp': 1775226100381, 'date': '2026-04-03T14:21:40.381Z', 'postedAgoShort': '13h', 'postedAgoText': '13 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "92",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Bhuvi IT Solutions",
    "status": "new",
    "posted": "{'timestamp': 1775243091568, 'date': '2026-04-03T19:04:51.568Z', 'postedAgoShort': '8h', 'postedAgoText': '8 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "93",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Melanie Borcher",
    "status": "new",
    "posted": "{'timestamp': 1773736989794, 'date': '2026-03-17T08:43:09.794Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "94",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Aishwarya Shinde",
    "status": "new",
    "posted": "{'timestamp': 1775135737213, 'date': '2026-04-02T13:15:37.213Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "95",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sourav Jinkalwad",
    "status": "new",
    "posted": "{'timestamp': 1775226770989, 'date': '2026-04-03T14:32:50.989Z', 'postedAgoShort': '13h', 'postedAgoText': '13 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "96",
    "title": "SAP Specialist",
    "company": "Empower Professionals, Inc.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ingit Mungi",
    "status": "new",
    "posted": "{'timestamp': 1775226335627, 'date': '2026-04-03T14:25:35.627Z', 'postedAgoShort': '13h', 'postedAgoText': '13 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "97",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "William Roske",
    "status": "new",
    "posted": "{'timestamp': 1773763124501, 'date': '2026-03-17T15:58:44.501Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "98",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "SyManSys Technologies India Pvt. Ltd.",
    "status": "new",
    "posted": "{'timestamp': 1775215728143, 'date': '2026-04-03T11:28:48.143Z', 'postedAgoShort': '16h', 'postedAgoText': '16 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "99",
    "title": "SAP Specialist",
    "company": "InterEx Group",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Madeline Brady",
    "status": "new",
    "posted": "{'timestamp': 1773415431885, 'date': '2026-03-13T15:23:51.885Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "100",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "ramesh Marri",
    "status": "new",
    "posted": "{'timestamp': 1775228247728, 'date': '2026-04-03T14:57:27.728Z', 'postedAgoShort': '12h', 'postedAgoText': '12 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "101",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Larissa Lima",
    "status": "new",
    "posted": "{'timestamp': 1775065099394, 'date': '2026-04-01T17:38:19.394Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "102",
    "title": "SAP Specialist",
    "company": "Bristlecone- A Mahindra Group Company",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Alok Adhikari",
    "status": "new",
    "posted": "{'timestamp': 1773727370522, 'date': '2026-03-17T06:02:50.522Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "103",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Live Connections",
    "status": "new",
    "posted": "{'timestamp': 1773574020573, 'date': '2026-03-15T11:27:00.573Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "104",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "durga kandharaboina",
    "status": "new",
    "posted": "{'timestamp': 1775217858798, 'date': '2026-04-03T12:04:18.798Z', 'postedAgoShort': '15h', 'postedAgoText': '15 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "105",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Paul Marrero",
    "status": "new",
    "posted": "{'timestamp': 1773360469777, 'date': '2026-03-13T00:07:49.777Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "106",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Anwar Ahmed",
    "status": "new",
    "posted": "{'timestamp': 1775224630787, 'date': '2026-04-03T13:57:10.787Z', 'postedAgoShort': '13h', 'postedAgoText': '13 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "107",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ben Taylor",
    "status": "new",
    "posted": "{'timestamp': 1775248956296, 'date': '2026-04-03T20:42:36.296Z', 'postedAgoShort': '7h', 'postedAgoText': '7 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "108",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ankit Giri",
    "status": "new",
    "posted": "{'timestamp': 1775225551724, 'date': '2026-04-03T14:12:31.724Z', 'postedAgoShort': '13h', 'postedAgoText': '13 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "109",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Naseer Akhtar",
    "status": "new",
    "posted": "{'timestamp': 1775213109188, 'date': '2026-04-03T10:45:09.188Z', 'postedAgoShort': '17h', 'postedAgoText': '17 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "110",
    "title": "SAP Specialist",
    "company": "Infosys | Ex- Cognizant |",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Deepak Dupaguntla",
    "status": "new",
    "posted": "{'timestamp': 1774766851272, 'date': '2026-03-29T06:47:31.272Z', 'postedAgoShort': '5d', 'postedAgoText': '5 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "111",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Deepa Sharma",
    "status": "new",
    "posted": "{'timestamp': 1774914106130, 'date': '2026-03-30T23:41:46.130Z', 'postedAgoShort': '4d', 'postedAgoText': '4 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "112",
    "title": "SAP Specialist",
    "company": "CAT Software Service Inc. \ud83d\udd0d Experienced Administrative Profe",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "M Azeem Uddin",
    "status": "new",
    "posted": "{'timestamp': 1775224414073, 'date': '2026-04-03T13:53:34.073Z', 'postedAgoShort': '13h', 'postedAgoText': '13 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "113",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "sakshi jadhav",
    "status": "new",
    "posted": "{'timestamp': 1774873104323, 'date': '2026-03-30T12:18:24.323Z', 'postedAgoShort': '4d', 'postedAgoText': '4 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "114",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Geeta M",
    "status": "new",
    "posted": "{'timestamp': 1775218147170, 'date': '2026-04-03T12:09:07.170Z', 'postedAgoShort': '15h', 'postedAgoText': '15 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "115",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Daya Madhurya Kandikatla",
    "status": "new",
    "posted": "{'timestamp': 1775221419158, 'date': '2026-04-03T13:03:39.158Z', 'postedAgoShort': '14h', 'postedAgoText': '14 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "116",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Daniel Andrews",
    "status": "new",
    "posted": "{'timestamp': 1772727753620, 'date': '2026-03-05T16:22:33.620Z', 'postedAgoShort': '4w', 'postedAgoText': '0 months ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "117",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "GrowthFn",
    "status": "new",
    "posted": "{'timestamp': 1775160115725, 'date': '2026-04-02T20:01:55.725Z', 'postedAgoShort': '17h', 'postedAgoText': '17 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "118",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jak Tompsett",
    "status": "new",
    "posted": "{'timestamp': 1775122630659, 'date': '2026-04-02T09:37:10.659Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "119",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Tom Cullen",
    "status": "new",
    "posted": "{'timestamp': 1773337235353, 'date': '2026-03-12T17:40:35.353Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "120",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Yin Pengcheng",
    "status": "new",
    "posted": "{'timestamp': 1774933699246, 'date': '2026-03-31T05:08:19.246Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "121",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sophia (Anu) Singh",
    "status": "new",
    "posted": "{'timestamp': 1773854141553, 'date': '2026-03-18T17:15:41.553Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "122",
    "title": "SAP Specialist",
    "company": "BlueRock Resources | \ud83d\udc8eSmarter Hiring in SAP, DATA & AI. Lowe",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Zane Grieve-Fitzell",
    "status": "new",
    "posted": "{'timestamp': 1773674107788, 'date': '2026-03-16T15:15:07.788Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "123",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Dr. Mahesh Kumar C.V.",
    "status": "new",
    "posted": "{'timestamp': 1773284406169, 'date': '2026-03-12T03:00:06.169Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "124",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Reading jobs, Berkshire",
    "status": "new",
    "posted": "{'timestamp': 1775214827167, 'date': '2026-04-03T11:13:47.167Z', 'postedAgoShort': '1h', 'postedAgoText': '1 hour ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "125",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Pavani N",
    "status": "new",
    "posted": "{'timestamp': 1775038021268, 'date': '2026-04-01T10:07:01.268Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "126",
    "title": "SAP Specialist",
    "company": "Whitehall Resources",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Emily Brett",
    "status": "new",
    "posted": "{'timestamp': 1773052167185, 'date': '2026-03-09T10:29:27.185Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "127",
    "title": "SAP Specialist",
    "company": "CoreVia | Full Cycle Recruitment Strategist | Talent Acquisi",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Munish Thakur",
    "status": "new",
    "posted": "{'timestamp': 1774024225655, 'date': '2026-03-20T16:30:25.655Z', 'postedAgoShort': '1w', 'postedAgoText': '1 week ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "128",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Everita Blanchette",
    "status": "new",
    "posted": "{'timestamp': 1773298681713, 'date': '2026-03-12T06:58:01.713Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "129",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Djilali FEGHOULI, PMP",
    "status": "new",
    "posted": "{'timestamp': 1773931917743, 'date': '2026-03-19T14:51:57.743Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "130",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Melanie Mehra",
    "status": "new",
    "posted": "{'timestamp': 1773843046985, 'date': '2026-03-18T14:10:46.985Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "131",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "VOXE",
    "status": "new",
    "posted": "{'timestamp': 1773052980794, 'date': '2026-03-09T10:43:00.794Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "132",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Katie Plowright",
    "status": "new",
    "posted": "{'timestamp': 1772638493847, 'date': '2026-03-04T15:34:53.847Z', 'postedAgoShort': '4w', 'postedAgoText': '0 months ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "133",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Drew Marshall",
    "status": "new",
    "posted": "{'timestamp': 1775150877948, 'date': '2026-04-02T17:27:57.948Z', 'postedAgoShort': '19h', 'postedAgoText': '19 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "134",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Rian Morgan",
    "status": "new",
    "posted": "{'timestamp': 1773740651766, 'date': '2026-03-17T09:44:11.766Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "135",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Hemanth H",
    "status": "new",
    "posted": "{'timestamp': 1773330786570, 'date': '2026-03-12T15:53:06.570Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "136",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Vartika Gupta",
    "status": "new",
    "posted": "{'timestamp': 1775100438381, 'date': '2026-04-02T03:27:18.381Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "137",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Indi Kitaure",
    "status": "new",
    "posted": "{'timestamp': 1775023225442, 'date': '2026-04-01T06:00:25.442Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "138",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Badarinadh Gelli",
    "status": "new",
    "posted": "{'timestamp': 1774931402978, 'date': '2026-03-31T04:30:02.978Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "139",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Abhay Singh",
    "status": "new",
    "posted": "{'timestamp': 1775021473398, 'date': '2026-04-01T05:31:13.398Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "140",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "MICKAEL QUESNOT",
    "status": "new",
    "posted": "{'timestamp': 1775131583540, 'date': '2026-04-02T12:06:23.540Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "141",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sachin Sharma",
    "status": "new",
    "posted": "{'timestamp': 1773072184043, 'date': '2026-03-09T16:03:04.043Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "142",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Lauren Gagliardi",
    "status": "new",
    "posted": "{'timestamp': 1774467902866, 'date': '2026-03-25T19:45:02.866Z', 'postedAgoShort': '1w', 'postedAgoText': '1 week ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "143",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "SAGE Business Solutions Inc.",
    "status": "new",
    "posted": "{'timestamp': 1775183105553, 'date': '2026-04-03T02:25:05.553Z', 'postedAgoShort': '10h', 'postedAgoText': '10 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "144",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sana Asher",
    "status": "new",
    "posted": "{'timestamp': 1775048486670, 'date': '2026-04-01T13:01:26.670Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "145",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "MICKAEL QUESNOT",
    "status": "new",
    "posted": "{'timestamp': 1774867148001, 'date': '2026-03-30T10:39:08.001Z', 'postedAgoShort': '4d', 'postedAgoText': '4 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "146",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Emma Adams",
    "status": "new",
    "posted": "{'timestamp': 1775032212061, 'date': '2026-04-01T08:30:12.061Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "147",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sachin Sharma",
    "status": "new",
    "posted": "{'timestamp': 1773677371724, 'date': '2026-03-16T16:09:31.724Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "148",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Luis R. Orecchia",
    "status": "new",
    "posted": "{'timestamp': 1774962967949, 'date': '2026-03-31T13:16:07.949Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "149",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jan Sirirat",
    "status": "new",
    "posted": "{'timestamp': 1773199925110, 'date': '2026-03-11T03:32:05.110Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "150",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Fazal N.",
    "status": "new",
    "posted": "{'timestamp': 1775139301599, 'date': '2026-04-02T14:15:01.599Z', 'postedAgoShort': '22h', 'postedAgoText': '22 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "151",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Pallavi G.",
    "status": "new",
    "posted": "{'timestamp': 1773638886151, 'date': '2026-03-16T05:28:06.151Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "152",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Vinay Pasalkar",
    "status": "new",
    "posted": "{'timestamp': 1775136478250, 'date': '2026-04-02T13:27:58.250Z', 'postedAgoShort': '23h', 'postedAgoText': '23 hours ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "153",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sachin Sharma",
    "status": "new",
    "posted": "{'timestamp': 1773075426577, 'date': '2026-03-09T16:57:06.577Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "154",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Wouter van Heddeghem",
    "status": "new",
    "posted": "{'timestamp': 1774974387007, 'date': '2026-03-31T16:26:27.007Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "155",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Fazal N.",
    "status": "new",
    "posted": "{'timestamp': 1775052902353, 'date': '2026-04-01T14:15:02.353Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "156",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Project School",
    "status": "new",
    "posted": "{'timestamp': 1774942663587, 'date': '2026-03-31T07:37:43.587Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "157",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "ConSAP",
    "status": "new",
    "posted": "{'timestamp': 1775081748616, 'date': '2026-04-01T22:15:48.616Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "158",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Callum George",
    "status": "new",
    "posted": "{'timestamp': 1774936808229, 'date': '2026-03-31T06:00:08.229Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "159",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Daniel Ross",
    "status": "new",
    "posted": "{'timestamp': 1774942208216, 'date': '2026-03-31T07:30:08.216Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "160",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Abhay Singh",
    "status": "new",
    "posted": "{'timestamp': 1774875746586, 'date': '2026-03-30T13:02:26.586Z', 'postedAgoShort': '4d', 'postedAgoText': '4 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "161",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jennifer Sosa Eskenazi",
    "status": "new",
    "posted": "{'timestamp': 1773833181248, 'date': '2026-03-18T11:26:21.248Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "162",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Hemant Rawat",
    "status": "new",
    "posted": "{'timestamp': 1773345136314, 'date': '2026-03-12T19:52:16.314Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "163",
    "title": "SAP Specialist",
    "company": "PRECISION ENTERPRISE",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Varsha Mavani",
    "status": "new",
    "posted": "{'timestamp': 1773587803123, 'date': '2026-03-15T15:16:43.123Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "164",
    "title": "SAP Specialist",
    "company": "Tata Technologies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ranjeeta. Sarkar",
    "status": "new",
    "posted": "{'timestamp': 1775129577843, 'date': '2026-04-02T11:32:57.843Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "165",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nitin Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1772985934422, 'date': '2026-03-08T16:05:34.422Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "166",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Akanksha Mengi",
    "status": "new",
    "posted": "{'timestamp': 1774946642700, 'date': '2026-03-31T08:44:02.700Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "167",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "LAXMIKANTH PATIL",
    "status": "new",
    "posted": "{'timestamp': 1775196761066, 'date': '2026-04-03T06:12:41.066Z', 'postedAgoShort': '6h', 'postedAgoText': '6 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "168",
    "title": "SAP Specialist",
    "company": "Tata Technologies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ranjeeta. Sarkar",
    "status": "new",
    "posted": "{'timestamp': 1775127643329, 'date': '2026-04-02T11:00:43.329Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "169",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sonali More",
    "status": "new",
    "posted": "{'timestamp': 1775042677629, 'date': '2026-04-01T11:24:37.629Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "170",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Suhayra D.",
    "status": "new",
    "posted": "{'timestamp': 1774960481013, 'date': '2026-03-31T12:34:41.013Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "171",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nitin Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1775063318834, 'date': '2026-04-01T17:08:38.834Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "172",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Dane Dan",
    "status": "new",
    "posted": "{'timestamp': 1774944361022, 'date': '2026-03-31T08:06:01.022Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "173",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "BK Pandey",
    "status": "new",
    "posted": "{'timestamp': 1775028344204, 'date': '2026-04-01T07:25:44.204Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "174",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Namrata Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1774011561271, 'date': '2026-03-20T12:59:21.271Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "175",
    "title": "SAP Specialist",
    "company": "PVRN Infosystems",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Lakshmi Devi S",
    "status": "new",
    "posted": "{'timestamp': 1775154405305, 'date': '2026-04-02T18:26:45.305Z', 'postedAgoShort': '18h', 'postedAgoText': '18 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "176",
    "title": "SAP Specialist",
    "company": "TotalTek | Connecting great people with meaningful SAP oppor",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "April Perez",
    "status": "new",
    "posted": "{'timestamp': 1773154126548, 'date': '2026-03-10T14:48:46.548Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "177",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nitin Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1774712774439, 'date': '2026-03-28T15:46:14.439Z', 'postedAgoShort': '5d', 'postedAgoText': '5 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "178",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Krishna Sameera V",
    "status": "new",
    "posted": "{'timestamp': 1775024387355, 'date': '2026-04-01T06:19:47.355Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "179",
    "title": "SAP Specialist",
    "company": "Accenture Federal Services",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Eric DeNicolis",
    "status": "new",
    "posted": "{'timestamp': 1775138947331, 'date': '2026-04-02T14:09:07.331Z', 'postedAgoShort': '23h', 'postedAgoText': '23 hours ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "180",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Melanie Borcher",
    "status": "new",
    "posted": "{'timestamp': 1773736989794, 'date': '2026-03-17T08:43:09.794Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "181",
    "title": "SAP Specialist",
    "company": "YASH Technologies | Connecting Top SAP Talent with Exception",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Samiksha Dubey",
    "status": "new",
    "posted": "{'timestamp': 1775116099694, 'date': '2026-04-02T07:48:19.694Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "182",
    "title": "SAP Specialist",
    "company": "Future Creation Placement Consultancy",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Mayuri Shinde",
    "status": "new",
    "posted": "{'timestamp': 1775105588116, 'date': '2026-04-02T04:53:08.116Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "183",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Bundy Baking Solutions",
    "status": "new",
    "posted": "{'timestamp': 1773930448853, 'date': '2026-03-19T14:27:28.853Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "184",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "IntVerse.io",
    "status": "new",
    "posted": "{'timestamp': 1773402973807, 'date': '2026-03-13T11:56:13.807Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "185",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Bente Grundt Hansen",
    "status": "new",
    "posted": "{'timestamp': 1773662303476, 'date': '2026-03-16T11:58:23.476Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "186",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Eunice Yang",
    "status": "new",
    "posted": "{'timestamp': 1775208437717, 'date': '2026-04-03T09:27:17.717Z', 'postedAgoShort': '3h', 'postedAgoText': '3 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "187",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Cyntia Jones, MPA, PMP, RTE",
    "status": "new",
    "posted": "{'timestamp': 1773860845190, 'date': '2026-03-18T19:07:25.190Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "188",
    "title": "SAP Specialist",
    "company": "Lynxmind",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Beatriz Pereira",
    "status": "new",
    "posted": "{'timestamp': 1775120417611, 'date': '2026-04-02T09:00:17.611Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "189",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Amer Ali",
    "status": "new",
    "posted": "{'timestamp': 1774958433854, 'date': '2026-03-31T12:00:33.854Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "190",
    "title": "SAP Specialist",
    "company": "Dexian | Part time Hockey Skills instructor & Coach of the 2",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Colin Clapton",
    "status": "new",
    "posted": "{'timestamp': 1773846312004, 'date': '2026-03-18T15:05:12.004Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "191",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Aadesh Soni",
    "status": "new",
    "posted": "{'timestamp': 1773750922895, 'date': '2026-03-17T12:35:22.895Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "192",
    "title": "SAP Specialist",
    "company": "MSP HITECT | Sourcing Talent Effectively",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "S. Sutha",
    "status": "new",
    "posted": "{'timestamp': 1773895555266, 'date': '2026-03-19T04:45:55.266Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "193",
    "title": "SAP Specialist",
    "company": "Investigo & Definia | SAP ERP | S/4HANA",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Lewis Dunn",
    "status": "new",
    "posted": "{'timestamp': 1773323397528, 'date': '2026-03-12T13:49:57.528Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "194",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Larissa Lima",
    "status": "new",
    "posted": "{'timestamp': 1775065099394, 'date': '2026-04-01T17:38:19.394Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "195",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Max Learmonth",
    "status": "new",
    "posted": "{'timestamp': 1775204440167, 'date': '2026-04-03T08:20:40.167Z', 'postedAgoShort': '4h', 'postedAgoText': '4 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "196",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "sudeeshna s",
    "status": "new",
    "posted": "{'timestamp': 1774071124998, 'date': '2026-03-21T05:32:04.998Z', 'postedAgoShort': '1w', 'postedAgoText': '1 week ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "197",
    "title": "SAP Specialist",
    "company": "InterEx Group",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Madeline Brady",
    "status": "new",
    "posted": "{'timestamp': 1773415431885, 'date': '2026-03-13T15:23:51.885Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "198",
    "title": "SAP Specialist",
    "company": "VHS professional services pvt ltd",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "FATHIMA BEEVI",
    "status": "new",
    "posted": "{'timestamp': 1775152358850, 'date': '2026-04-02T17:52:38.850Z', 'postedAgoShort': '19h', 'postedAgoText': '19 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "199",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Live Connections",
    "status": "new",
    "posted": "{'timestamp': 1773574020573, 'date': '2026-03-15T11:27:00.573Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "200",
    "title": "SAP Specialist",
    "company": "Augusta Hitech",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Karishma Wadhwani",
    "status": "new",
    "posted": "{'timestamp': 1775169858267, 'date': '2026-04-02T22:44:18.267Z', 'postedAgoShort': '14h', 'postedAgoText': '14 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "201",
    "title": "SAP Specialist",
    "company": "Bristlecone- A Mahindra Group Company",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Alok Adhikari",
    "status": "new",
    "posted": "{'timestamp': 1773727370522, 'date': '2026-03-17T06:02:50.522Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "202",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Narcis Gabriel Velcu",
    "status": "new",
    "posted": "{'timestamp': 1773821924406, 'date': '2026-03-18T08:18:44.406Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "203",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Paul Marrero",
    "status": "new",
    "posted": "{'timestamp': 1773360469777, 'date': '2026-03-13T00:07:49.777Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "204",
    "title": "SAP Specialist",
    "company": "Trinity Consulting Services (\"TRINITY\")",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sharon Jedediah",
    "status": "new",
    "posted": "{'timestamp': 1773824523369, 'date': '2026-03-18T09:02:03.369Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "205",
    "title": "SAP Specialist",
    "company": "Future Creation Group Of Companies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sakshi K",
    "status": "new",
    "posted": "{'timestamp': 1775150843381, 'date': '2026-04-02T17:27:23.381Z', 'postedAgoShort': '19h', 'postedAgoText': '19 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "206",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Craig Brown",
    "status": "new",
    "posted": "{'timestamp': 1773680397565, 'date': '2026-03-16T16:59:57.565Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "207",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Lalitha Tejaswini Batchu",
    "status": "new",
    "posted": "{'timestamp': 1774853327894, 'date': '2026-03-30T06:48:47.894Z', 'postedAgoShort': '4d', 'postedAgoText': '4 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "208",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Pavan Shankar",
    "status": "new",
    "posted": "{'timestamp': 1773669672422, 'date': '2026-03-16T14:01:12.422Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "209",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Priyanka Pandey",
    "status": "new",
    "posted": "{'timestamp': 1773992276785, 'date': '2026-03-20T07:37:56.785Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "210",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "SyManSys Technologies India Pvt. Ltd.",
    "status": "new",
    "posted": "{'timestamp': 1775215728143, 'date': '2026-04-03T11:28:48.143Z', 'postedAgoShort': '1h', 'postedAgoText': '1 hour ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "211",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "ITC Infotech Jobs",
    "status": "new",
    "posted": "{'timestamp': 1773830415781, 'date': '2026-03-18T10:40:15.781Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "212",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "William Roske",
    "status": "new",
    "posted": "{'timestamp': 1773763124501, 'date': '2026-03-17T15:58:44.501Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "213",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Priya Kedia",
    "status": "new",
    "posted": "{'timestamp': 1775190710326, 'date': '2026-04-03T04:31:50.326Z', 'postedAgoShort': '8h', 'postedAgoText': '8 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "214",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Raveena Mourya",
    "status": "new",
    "posted": "{'timestamp': 1775145162206, 'date': '2026-04-02T15:52:42.206Z', 'postedAgoShort': '21h', 'postedAgoText': '21 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "215",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Katia Choquette",
    "status": "new",
    "posted": "{'timestamp': 1774999801181, 'date': '2026-03-31T23:30:01.181Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "216",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jennifer Sosa Eskenazi",
    "status": "new",
    "posted": "{'timestamp': 1773833181248, 'date': '2026-03-18T11:26:21.248Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "217",
    "title": "SAP Specialist",
    "company": "PRECISION ENTERPRISE",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Varsha Mavani",
    "status": "new",
    "posted": "{'timestamp': 1773587803123, 'date': '2026-03-15T15:16:43.123Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "218",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Suhayra D.",
    "status": "new",
    "posted": "{'timestamp': 1774960481013, 'date': '2026-03-31T12:34:41.013Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "219",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Tanya Kharb",
    "status": "new",
    "posted": "{'timestamp': 1775144239484, 'date': '2026-04-02T15:37:19.484Z', 'postedAgoShort': '11h', 'postedAgoText': '11 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "220",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Akanksha Mengi",
    "status": "new",
    "posted": "{'timestamp': 1774946642700, 'date': '2026-03-31T08:44:02.700Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "221",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Lisa Bose",
    "status": "new",
    "posted": "{'timestamp': 1773715651633, 'date': '2026-03-17T02:47:31.633Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "222",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nitin Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1772985934422, 'date': '2026-03-08T16:05:34.422Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "223",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Magnify360 Hi-Tech Solutions Pvt. Ltd",
    "status": "new",
    "posted": "{'timestamp': 1775019351988, 'date': '2026-04-01T04:55:51.988Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "224",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nilesh Suryavanshi",
    "status": "new",
    "posted": "{'timestamp': 1775123183155, 'date': '2026-04-02T09:46:23.155Z', 'postedAgoShort': '17h', 'postedAgoText': '17 hours ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "225",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Janejira Laobuaban",
    "status": "new",
    "posted": "{'timestamp': 1775111074906, 'date': '2026-04-02T06:24:34.906Z', 'postedAgoShort': '21h', 'postedAgoText': '21 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "226",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Harshini Veladi",
    "status": "new",
    "posted": "{'timestamp': 1775132999794, 'date': '2026-04-02T12:29:59.794Z', 'postedAgoShort': '15h', 'postedAgoText': '15 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "227",
    "title": "SAP Specialist",
    "company": "Future Creation Placement Consultancy",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Mayuri Shinde",
    "status": "new",
    "posted": "{'timestamp': 1775105588116, 'date': '2026-04-02T04:53:08.116Z', 'postedAgoShort': '22h', 'postedAgoText': '22 hours ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "228",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Soniya E",
    "status": "new",
    "posted": "{'timestamp': 1775148830137, 'date': '2026-04-02T16:53:50.137Z', 'postedAgoShort': '10h', 'postedAgoText': '10 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "229",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Reading jobs, Berkshire",
    "status": "new",
    "posted": "{'timestamp': 1775127155308, 'date': '2026-04-02T10:52:35.308Z', 'postedAgoShort': '16h', 'postedAgoText': '16 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "230",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Look4IT",
    "status": "new",
    "posted": "{'timestamp': 1775129301330, 'date': '2026-04-02T11:28:21.330Z', 'postedAgoShort': '16h', 'postedAgoText': '16 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "231",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Neha Khanna",
    "status": "new",
    "posted": "{'timestamp': 1775127475705, 'date': '2026-04-02T10:57:55.705Z', 'postedAgoShort': '16h', 'postedAgoText': '16 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "232",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Djilali FEGHOULI, PMP",
    "status": "new",
    "posted": "{'timestamp': 1773931917743, 'date': '2026-03-19T14:51:57.743Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "233",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "P SAIKRISHNA",
    "status": "new",
    "posted": "{'timestamp': 1775142880330, 'date': '2026-04-02T15:14:40.330Z', 'postedAgoShort': '12h', 'postedAgoText': '12 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "234",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Daniel Andrews",
    "status": "new",
    "posted": "{'timestamp': 1772727753620, 'date': '2026-03-05T16:22:33.620Z', 'postedAgoShort': '4w', 'postedAgoText': '0 months ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "235",
    "title": "SAP Specialist",
    "company": "ROITech||Hiring for IT professionals||SAP MODULES||Hiring To",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Shalini Sanyal",
    "status": "new",
    "posted": "{'timestamp': 1775126587214, 'date': '2026-04-02T10:43:07.214Z', 'postedAgoShort': '16h', 'postedAgoText': '16 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "236",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Yin Pengcheng",
    "status": "new",
    "posted": "{'timestamp': 1774931690909, 'date': '2026-03-31T04:34:50.909Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "237",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "BK Pandey",
    "status": "new",
    "posted": "{'timestamp': 1775028344204, 'date': '2026-04-01T07:25:44.204Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "238",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "sujata verma",
    "status": "new",
    "posted": "{'timestamp': 1775151971465, 'date': '2026-04-02T17:46:11.465Z', 'postedAgoShort': '9h', 'postedAgoText': '9 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "239",
    "title": "SAP Specialist",
    "company": "BlueRock Resources | \ud83d\udc8eSmarter Hiring in SAP, DATA & AI. Lowe",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Zane Grieve-Fitzell",
    "status": "new",
    "posted": "{'timestamp': 1773674107788, 'date': '2026-03-16T15:15:07.788Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "240",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sirisha Patnaik",
    "status": "new",
    "posted": "{'timestamp': 1775143146273, 'date': '2026-04-02T15:19:06.273Z', 'postedAgoShort': '12h', 'postedAgoText': '12 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "241",
    "title": "SAP Specialist",
    "company": "Qualite manpower",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Swati Kushwah",
    "status": "new",
    "posted": "{'timestamp': 1775121760292, 'date': '2026-04-02T09:22:40.292Z', 'postedAgoShort': '18h', 'postedAgoText': '18 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "242",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sunetra Ray",
    "status": "new",
    "posted": "{'timestamp': 1775131723149, 'date': '2026-04-02T12:08:43.149Z', 'postedAgoShort': '15h', 'postedAgoText': '15 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "243",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Krishna Sameera V",
    "status": "new",
    "posted": "{'timestamp': 1775024387355, 'date': '2026-04-01T06:19:47.355Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "244",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Rian Morgan",
    "status": "new",
    "posted": "{'timestamp': 1773740651766, 'date': '2026-03-17T09:44:11.766Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "245",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Kevin Agu",
    "status": "new",
    "posted": "{'timestamp': 1775160226798, 'date': '2026-04-02T20:03:46.798Z', 'postedAgoShort': '7h', 'postedAgoText': '7 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "246",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Namrata Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1774011561271, 'date': '2026-03-20T12:59:21.271Z', 'postedAgoShort': '1w', 'postedAgoText': '1 week ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "247",
    "title": "SAP Specialist",
    "company": "JKV International working on C2C and W2 Positions",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Srihari Jonnalagadda",
    "status": "new",
    "posted": "{'timestamp': 1775160625562, 'date': '2026-04-02T20:10:25.562Z', 'postedAgoShort': '7h', 'postedAgoText': '7 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "248",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Everita Blanchette",
    "status": "new",
    "posted": "{'timestamp': 1773298681713, 'date': '2026-03-12T06:58:01.713Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "249",
    "title": "SAP Specialist",
    "company": "Tata Technologies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ranjeeta. Sarkar",
    "status": "new",
    "posted": "{'timestamp': 1775129577843, 'date': '2026-04-02T11:32:57.843Z', 'postedAgoShort': '15h', 'postedAgoText': '15 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "250",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jak Tompsett",
    "status": "new",
    "posted": "{'timestamp': 1775122630659, 'date': '2026-04-02T09:37:10.659Z', 'postedAgoShort': '17h', 'postedAgoText': '17 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "251",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sonali More",
    "status": "new",
    "posted": "{'timestamp': 1775042677629, 'date': '2026-04-01T11:24:37.629Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "252",
    "title": "SAP Specialist",
    "company": "Tata Technologies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ranjeeta. Sarkar",
    "status": "new",
    "posted": "{'timestamp': 1775127643329, 'date': '2026-04-02T11:00:43.329Z', 'postedAgoShort': '16h', 'postedAgoText': '16 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "253",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Rupal Pandey",
    "status": "new",
    "posted": "{'timestamp': 1775144688931, 'date': '2026-04-02T15:44:48.931Z', 'postedAgoShort': '11h', 'postedAgoText': '11 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "254",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Rashmi Deshpande",
    "status": "new",
    "posted": "{'timestamp': 1773725463378, 'date': '2026-03-17T05:31:03.378Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "255",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Katie Plowright",
    "status": "new",
    "posted": "{'timestamp': 1772638493847, 'date': '2026-03-04T15:34:53.847Z', 'postedAgoShort': '4w', 'postedAgoText': '0 months ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "256",
    "title": "SAP Specialist",
    "company": "CoreVia | Full Cycle Recruitment Strategist | Talent Acquisi",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Munish Thakur",
    "status": "new",
    "posted": "{'timestamp': 1774024225655, 'date': '2026-03-20T16:30:25.655Z', 'postedAgoShort': '1w', 'postedAgoText': '1 week ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "257",
    "title": "SAP Specialist",
    "company": "Tanisha Systems, Inc",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Naveen Verma",
    "status": "new",
    "posted": "{'timestamp': 1775150118315, 'date': '2026-04-02T17:15:18.315Z', 'postedAgoShort': '10h', 'postedAgoText': '10 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "258",
    "title": "SAP Specialist",
    "company": "JK Technohub - HR recruitment company, we are providing- Res",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Rajiv Gupta",
    "status": "new",
    "posted": "{'timestamp': 1774810568620, 'date': '2026-03-29T18:56:08.620Z', 'postedAgoShort': '4d', 'postedAgoText': '4 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "259",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Hemanth H",
    "status": "new",
    "posted": "{'timestamp': 1773330786570, 'date': '2026-03-12T15:53:06.570Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "260",
    "title": "SAP Specialist",
    "company": "Workcog Inc | Sr.IT Recruitment, Hiring",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Prasanna Raj",
    "status": "new",
    "posted": "{'timestamp': 1775146618745, 'date': '2026-04-02T16:16:58.745Z', 'postedAgoShort': '11h', 'postedAgoText': '11 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "261",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nitin Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1774712774439, 'date': '2026-03-28T15:46:14.439Z', 'postedAgoShort': '5d', 'postedAgoText': '5 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "262",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Suresh Kondapalli",
    "status": "new",
    "posted": "{'timestamp': 1775142678738, 'date': '2026-04-02T15:11:18.738Z', 'postedAgoShort': '12h', 'postedAgoText': '12 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "263",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Dr. Mahesh Kumar C.V.",
    "status": "new",
    "posted": "{'timestamp': 1773284406169, 'date': '2026-03-12T03:00:06.169Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "264",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Aray Consulting LLP",
    "status": "new",
    "posted": "{'timestamp': 1775124998296, 'date': '2026-04-02T10:16:38.296Z', 'postedAgoShort': '17h', 'postedAgoText': '17 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "265",
    "title": "SAP Specialist",
    "company": "JKV International",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "prudhvi pulivarthi",
    "status": "new",
    "posted": "{'timestamp': 1775161548133, 'date': '2026-04-02T20:25:48.133Z', 'postedAgoShort': '7h', 'postedAgoText': '7 hours ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "266",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Drew Marshall",
    "status": "new",
    "posted": "{'timestamp': 1775150877948, 'date': '2026-04-02T17:27:57.948Z', 'postedAgoShort': '10h', 'postedAgoText': '10 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "267",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Vartika Gupta",
    "status": "new",
    "posted": "{'timestamp': 1775100438381, 'date': '2026-04-02T03:27:18.381Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "268",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Melanie Mehra",
    "status": "new",
    "posted": "{'timestamp': 1773843046985, 'date': '2026-03-18T14:10:46.985Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "269",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Amita Dwivedi",
    "status": "new",
    "posted": "{'timestamp': 1775143785867, 'date': '2026-04-02T15:29:45.867Z', 'postedAgoShort': '12h', 'postedAgoText': '12 hours ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "270",
    "title": "SAP Specialist",
    "company": "GrowthFn Malaysia. I am hiring IT & Non - IT Roles: Malaysia",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Afeez Owolabi",
    "status": "new",
    "posted": "{'timestamp': 1775160001081, 'date': '2026-04-02T20:00:01.081Z', 'postedAgoShort': '7h', 'postedAgoText': '7 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "271",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Pavani N",
    "status": "new",
    "posted": "{'timestamp': 1775038021268, 'date': '2026-04-01T10:07:01.268Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "272",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Karan Chandra Kothari",
    "status": "new",
    "posted": "{'timestamp': 1775147403513, 'date': '2026-04-02T16:30:03.513Z', 'postedAgoShort': '11h', 'postedAgoText': '11 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "273",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nitin Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1775063318834, 'date': '2026-04-01T17:08:38.834Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "274",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "VOXE",
    "status": "new",
    "posted": "{'timestamp': 1773052980794, 'date': '2026-03-09T10:43:00.794Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "275",
    "title": "SAP Specialist",
    "company": "Whitehall Resources",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Emily Brett",
    "status": "new",
    "posted": "{'timestamp': 1773052167185, 'date': '2026-03-09T10:29:27.185Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "276",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Dane Dan",
    "status": "new",
    "posted": "{'timestamp': 1774944361022, 'date': '2026-03-31T08:06:01.022Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "277",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Bhanu Prakash",
    "status": "new",
    "posted": "{'timestamp': 1775141651689, 'date': '2026-04-02T14:54:11.689Z', 'postedAgoShort': '12h', 'postedAgoText': '12 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "278",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sophia (Anu) Singh",
    "status": "new",
    "posted": "{'timestamp': 1773854141553, 'date': '2026-03-18T17:15:41.553Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "279",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Tom Cullen",
    "status": "new",
    "posted": "{'timestamp': 1773337235353, 'date': '2026-03-12T17:40:35.353Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "280",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Arjit Sharma",
    "status": "new",
    "posted": "{'timestamp': 1775148730307, 'date': '2026-04-02T16:52:10.307Z', 'postedAgoShort': '10h', 'postedAgoText': '10 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "281",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "GrowthFn",
    "status": "new",
    "posted": "{'timestamp': 1775160115725, 'date': '2026-04-02T20:01:55.725Z', 'postedAgoShort': '7h', 'postedAgoText': '7 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "282",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ramya Raghu",
    "status": "new",
    "posted": "{'timestamp': 1775029045235, 'date': '2026-04-01T07:37:25.235Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "283",
    "title": "SAP Specialist",
    "company": "Fixity Technologies | IT Recruitment",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Junaid khan",
    "status": "new",
    "posted": "{'timestamp': 1775158461287, 'date': '2026-04-02T19:34:21.287Z', 'postedAgoShort': '7h', 'postedAgoText': '7 hours ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "284",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Pallavi G.",
    "status": "new",
    "posted": "{'timestamp': 1773638886151, 'date': '2026-03-16T05:28:06.151Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "285",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "SAP Jobs in Germany",
    "status": "new",
    "posted": "{'timestamp': 1775127696621, 'date': '2026-04-02T11:01:36.621Z', 'postedAgoShort': '16h', 'postedAgoText': '16 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "286",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Callum George",
    "status": "new",
    "posted": "{'timestamp': 1774936808229, 'date': '2026-03-31T06:00:08.229Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "287",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Chimala Neelaveni",
    "status": "new",
    "posted": "{'timestamp': 1775110909221, 'date': '2026-04-02T06:21:49.221Z', 'postedAgoShort': '21h', 'postedAgoText': '21 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "288",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "SAGE Business Solutions Inc.",
    "status": "new",
    "posted": "{'timestamp': 1775183105553, 'date': '2026-04-03T02:25:05.553Z', 'postedAgoShort': '1h', 'postedAgoText': '1 hour ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "289",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sachin Sharma",
    "status": "new",
    "posted": "{'timestamp': 1773075426577, 'date': '2026-03-09T16:57:06.577Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "290",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jan Sirirat",
    "status": "new",
    "posted": "{'timestamp': 1773199925110, 'date': '2026-03-11T03:32:05.110Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "291",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Fazal N.",
    "status": "new",
    "posted": "{'timestamp': 1775052902353, 'date': '2026-04-01T14:15:02.353Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "292",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Lauren Gagliardi",
    "status": "new",
    "posted": "{'timestamp': 1774467902866, 'date': '2026-03-25T19:45:02.866Z', 'postedAgoShort': '1w', 'postedAgoText': '1 week ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "293",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Indi Kitaure",
    "status": "new",
    "posted": "{'timestamp': 1775023225442, 'date': '2026-04-01T06:00:25.442Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "294",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Luis R. Orecchia",
    "status": "new",
    "posted": "{'timestamp': 1774962967949, 'date': '2026-03-31T13:16:07.949Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "295",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sachin Sharma",
    "status": "new",
    "posted": "{'timestamp': 1773072184043, 'date': '2026-03-09T16:03:04.043Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "296",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Abhay Singh",
    "status": "new",
    "posted": "{'timestamp': 1774875746586, 'date': '2026-03-30T13:02:26.586Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "297",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sachin Sharma",
    "status": "new",
    "posted": "{'timestamp': 1773677371724, 'date': '2026-03-16T16:09:31.724Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "298",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sana Asher",
    "status": "new",
    "posted": "{'timestamp': 1775048486670, 'date': '2026-04-01T13:01:26.670Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "299",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "MICKAEL QUESNOT",
    "status": "new",
    "posted": "{'timestamp': 1774867148001, 'date': '2026-03-30T10:39:08.001Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "300",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Badarinadh Gelli",
    "status": "new",
    "posted": "{'timestamp': 1774931402978, 'date': '2026-03-31T04:30:02.978Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "301",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Project School",
    "status": "new",
    "posted": "{'timestamp': 1774942663587, 'date': '2026-03-31T07:37:43.587Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "302",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "ConSAP",
    "status": "new",
    "posted": "{'timestamp': 1775081748616, 'date': '2026-04-01T22:15:48.616Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "303",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Wouter van Heddeghem",
    "status": "new",
    "posted": "{'timestamp': 1774974387007, 'date': '2026-03-31T16:26:27.007Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "304",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Emma Adams",
    "status": "new",
    "posted": "{'timestamp': 1775032212061, 'date': '2026-04-01T08:30:12.061Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "305",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Fazal N.",
    "status": "new",
    "posted": "{'timestamp': 1775139301599, 'date': '2026-04-02T14:15:01.599Z', 'postedAgoShort': '13h', 'postedAgoText': '13 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "306",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Abhay Singh",
    "status": "new",
    "posted": "{'timestamp': 1775021473398, 'date': '2026-04-01T05:31:13.398Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "307",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Vinay Pasalkar",
    "status": "new",
    "posted": "{'timestamp': 1775136478250, 'date': '2026-04-02T13:27:58.250Z', 'postedAgoShort': '14h', 'postedAgoText': '14 hours ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "308",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Daniel Ross",
    "status": "new",
    "posted": "{'timestamp': 1774942208216, 'date': '2026-03-31T07:30:08.216Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "309",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "MICKAEL QUESNOT",
    "status": "new",
    "posted": "{'timestamp': 1775131583540, 'date': '2026-04-02T12:06:23.540Z', 'postedAgoShort': '15h', 'postedAgoText': '15 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "310",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Katia Choquette",
    "status": "new",
    "posted": "{'timestamp': 1774999801181, 'date': '2026-03-31T23:30:01.181Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "311",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Mriti InfoSystems Inc.",
    "status": "new",
    "posted": "{'timestamp': 1775129032544, 'date': '2026-04-02T11:23:52.544Z', 'postedAgoShort': '16h', 'postedAgoText': '16 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "312",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Kirithika Karthikeyan",
    "status": "new",
    "posted": "{'timestamp': 1775133621465, 'date': '2026-04-02T12:40:21.465Z', 'postedAgoShort': '14h', 'postedAgoText': '14 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "313",
    "title": "SAP Specialist",
    "company": "OLM Consultants | International Recruitment",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Morten Carstensen",
    "status": "new",
    "posted": "{'timestamp': 1775122629149, 'date': '2026-04-02T09:37:09.149Z', 'postedAgoShort': '17h', 'postedAgoText': '17 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "314",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Larissa Lima",
    "status": "new",
    "posted": "{'timestamp': 1775065099394, 'date': '2026-04-01T17:38:19.394Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "315",
    "title": "SAP Specialist",
    "company": "YASH Technologies | Connecting Top SAP Talent with Exception",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Samiksha Dubey",
    "status": "new",
    "posted": "{'timestamp': 1775116325076, 'date': '2026-04-02T07:52:05.076Z', 'postedAgoShort': '19h', 'postedAgoText': '19 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "316",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Aditi Malik",
    "status": "new",
    "posted": "{'timestamp': 1775135477528, 'date': '2026-04-02T13:11:17.528Z', 'postedAgoShort': '14h', 'postedAgoText': '14 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "317",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Amer Ali",
    "status": "new",
    "posted": "{'timestamp': 1774958433854, 'date': '2026-03-31T12:00:33.854Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "318",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Paul Marrero",
    "status": "new",
    "posted": "{'timestamp': 1773360469777, 'date': '2026-03-13T00:07:49.777Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "319",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Lauren Stutz",
    "status": "new",
    "posted": "{'timestamp': 1774866611116, 'date': '2026-03-30T10:30:11.116Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "320",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "VirtoTech",
    "status": "new",
    "posted": "{'timestamp': 1775126095682, 'date': '2026-04-02T10:34:55.682Z', 'postedAgoShort': '16h', 'postedAgoText': '16 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "321",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Lakshmi Ippili",
    "status": "new",
    "posted": "{'timestamp': 1775124919104, 'date': '2026-04-02T10:15:19.104Z', 'postedAgoShort': '17h', 'postedAgoText': '17 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "322",
    "title": "SAP Specialist",
    "company": "Future Creation Group Of Companies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sakshi K",
    "status": "new",
    "posted": "{'timestamp': 1775150843381, 'date': '2026-04-02T17:27:23.381Z', 'postedAgoShort': '10h', 'postedAgoText': '10 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "323",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "IntVerse.io",
    "status": "new",
    "posted": "{'timestamp': 1775151271000, 'date': '2026-04-02T17:34:31.000Z', 'postedAgoShort': '9h', 'postedAgoText': '9 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "324",
    "title": "SAP Specialist",
    "company": "Jconnect Infotech Inc | Technical Recruiting",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jatin Yadav",
    "status": "new",
    "posted": "{'timestamp': 1775169361000, 'date': '2026-04-02T22:36:01.000Z', 'postedAgoShort': '4h', 'postedAgoText': '4 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "325",
    "title": "SAP Specialist",
    "company": "Dexian | Part time Hockey Skills instructor & Coach of the 2",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Colin Clapton",
    "status": "new",
    "posted": "{'timestamp': 1773846312004, 'date': '2026-03-18T15:05:12.004Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "326",
    "title": "SAP Specialist",
    "company": "Augusta Hitech",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Karishma Wadhwani",
    "status": "new",
    "posted": "{'timestamp': 1775169858267, 'date': '2026-04-02T22:44:18.267Z', 'postedAgoShort': '4h', 'postedAgoText': '4 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "327",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "William Roske",
    "status": "new",
    "posted": "{'timestamp': 1773763124501, 'date': '2026-03-17T15:58:44.501Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "328",
    "title": "SAP Specialist",
    "company": "InterEx Group",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Madeline Brady",
    "status": "new",
    "posted": "{'timestamp': 1773415431885, 'date': '2026-03-13T15:23:51.885Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "329",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Deepa Sharma",
    "status": "new",
    "posted": "{'timestamp': 1774914106130, 'date': '2026-03-30T23:41:46.130Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "330",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Deepak chaudhary",
    "status": "new",
    "posted": "{'timestamp': 1775152966897, 'date': '2026-04-02T18:02:46.897Z', 'postedAgoShort': '9h', 'postedAgoText': '9 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "331",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "HR Codetech",
    "status": "new",
    "posted": "{'timestamp': 1775153467846, 'date': '2026-04-02T18:11:07.846Z', 'postedAgoShort': '9h', 'postedAgoText': '9 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "332",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ellie Sapstead",
    "status": "new",
    "posted": "{'timestamp': 1775125632946, 'date': '2026-04-02T10:27:12.946Z', 'postedAgoShort': '17h', 'postedAgoText': '17 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "333",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "sakshi jadhav",
    "status": "new",
    "posted": "{'timestamp': 1774873104323, 'date': '2026-03-30T12:18:24.323Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "334",
    "title": "SAP Specialist",
    "company": "MASE Insights",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Rupa kumari Agala",
    "status": "new",
    "posted": "{'timestamp': 1775135879255, 'date': '2026-04-02T13:17:59.255Z', 'postedAgoShort': '14h', 'postedAgoText': '14 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "335",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "FAIR Consulting Group",
    "status": "new",
    "posted": "{'timestamp': 1775112495940, 'date': '2026-04-02T06:48:15.940Z', 'postedAgoShort': '20h', 'postedAgoText': '20 hours ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "336",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Cyntia Jones, MPA, PMP, RTE",
    "status": "new",
    "posted": "{'timestamp': 1773860845190, 'date': '2026-03-18T19:07:25.190Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "337",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Raja Rajarajan",
    "status": "new",
    "posted": "{'timestamp': 1775163855066, 'date': '2026-04-02T21:04:15.066Z', 'postedAgoShort': '6h', 'postedAgoText': '6 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "338",
    "title": "SAP Specialist",
    "company": "Future Creation Group Of Companies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sakshi K",
    "status": "new",
    "posted": "{'timestamp': 1775119077471, 'date': '2026-04-02T08:37:57.471Z', 'postedAgoShort': '18h', 'postedAgoText': '18 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "339",
    "title": "SAP Specialist",
    "company": "Infosys | Ex- Cognizant |",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Deepak Dupaguntla",
    "status": "new",
    "posted": "{'timestamp': 1774766851272, 'date': '2026-03-29T06:47:31.272Z', 'postedAgoShort': '4d', 'postedAgoText': '4 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "340",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Satwika .",
    "status": "new",
    "posted": "{'timestamp': 1775155586191, 'date': '2026-04-02T18:46:26.191Z', 'postedAgoShort': '8h', 'postedAgoText': '8 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "341",
    "title": "SAP Specialist",
    "company": "Krishna Memorial Trust",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Prakhar .",
    "status": "new",
    "posted": "{'timestamp': 1774940305584, 'date': '2026-03-31T06:58:25.584Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "342",
    "title": "SAP Specialist",
    "company": "Bristlecone- A Mahindra Group Company",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Alok Adhikari",
    "status": "new",
    "posted": "{'timestamp': 1773727370522, 'date': '2026-03-17T06:02:50.522Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "343",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Mohit Pal",
    "status": "new",
    "posted": "{'timestamp': 1775157178382, 'date': '2026-04-02T19:12:58.382Z', 'postedAgoShort': '8h', 'postedAgoText': '8 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "344",
    "title": "SAP Specialist",
    "company": "USM | Full Life Cycle Recruiting",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Lakshmikantha N",
    "status": "new",
    "posted": "{'timestamp': 1773433055822, 'date': '2026-03-13T20:17:35.822Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "345",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Daniel Andrews",
    "status": "new",
    "posted": "{'timestamp': 1772727753620, 'date': '2026-03-05T16:22:33.620Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "346",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Dr. Mahesh Kumar C.V.",
    "status": "new",
    "posted": "{'timestamp': 1773284406169, 'date': '2026-03-12T03:00:06.169Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "347",
    "title": "SAP Specialist",
    "company": "Whitehall Resources",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Emily Brett",
    "status": "new",
    "posted": "{'timestamp': 1773052167185, 'date': '2026-03-09T10:29:27.185Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "348",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Djilali FEGHOULI, PMP",
    "status": "new",
    "posted": "{'timestamp': 1773931917743, 'date': '2026-03-19T14:51:57.743Z', 'postedAgoShort': '1w', 'postedAgoText': '1 week ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "349",
    "title": "SAP Specialist",
    "company": "Meeden Labs | BE in Computer Engineering",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Soni K.",
    "status": "new",
    "posted": "{'timestamp': 1772687430234, 'date': '2026-03-05T05:10:30.234Z', 'postedAgoShort': '4w', 'postedAgoText': '0 months ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "350",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Katie Plowright",
    "status": "new",
    "posted": "{'timestamp': 1772638493847, 'date': '2026-03-04T15:34:53.847Z', 'postedAgoShort': '4w', 'postedAgoText': '0 months ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "351",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ritik Sahu",
    "status": "new",
    "posted": "{'timestamp': 1774552616844, 'date': '2026-03-26T19:16:56.844Z', 'postedAgoShort': '6d', 'postedAgoText': '6 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "352",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Tom Cullen",
    "status": "new",
    "posted": "{'timestamp': 1773337235353, 'date': '2026-03-12T17:40:35.353Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "353",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Reading jobs, Berkshire",
    "status": "new",
    "posted": "{'timestamp': 1775044404446, 'date': '2026-04-01T11:53:24.446Z', 'postedAgoShort': '22h', 'postedAgoText': '22 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "354",
    "title": "SAP Specialist",
    "company": "DruNix Solutions & Tech-IM Pro Services | 15+ Years US IT St",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Srinivas M",
    "status": "new",
    "posted": "{'timestamp': 1773942823087, 'date': '2026-03-19T17:53:43.087Z', 'postedAgoShort': '1w', 'postedAgoText': '1 week ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "355",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Bipasha Das",
    "status": "new",
    "posted": "{'timestamp': 1775019423620, 'date': '2026-04-01T04:57:03.620Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "356",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Yin Pengcheng",
    "status": "new",
    "posted": "{'timestamp': 1775050151805, 'date': '2026-04-01T13:29:11.805Z', 'postedAgoShort': '20h', 'postedAgoText': '20 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "357",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Praveen R.",
    "status": "new",
    "posted": "{'timestamp': 1775054331715, 'date': '2026-04-01T14:38:51.715Z', 'postedAgoShort': '19h', 'postedAgoText': '19 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "358",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jak Tompsett",
    "status": "new",
    "posted": "{'timestamp': 1775122630659, 'date': '2026-04-02T09:37:10.659Z', 'postedAgoShort': '31m', 'postedAgoText': '31 minutes ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "359",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ajit Deshpande",
    "status": "new",
    "posted": "{'timestamp': 1775076913149, 'date': '2026-04-01T20:55:13.149Z', 'postedAgoShort': '13h', 'postedAgoText': '13 hours ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "360",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ruby S Raghav",
    "status": "new",
    "posted": "{'timestamp': 1775049938960, 'date': '2026-04-01T13:25:38.960Z', 'postedAgoShort': '20h', 'postedAgoText': '20 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "361",
    "title": "SAP Specialist",
    "company": "OLM Consultants | International Recruitment",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Morten Carstensen",
    "status": "new",
    "posted": "{'timestamp': 1775122629149, 'date': '2026-04-02T09:37:09.149Z', 'postedAgoShort': '31m', 'postedAgoText': '31 minutes ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "362",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Rian Morgan",
    "status": "new",
    "posted": "{'timestamp': 1773740651766, 'date': '2026-03-17T09:44:11.766Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "363",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ramanpreet Kaur",
    "status": "new",
    "posted": "{'timestamp': 1775062305191, 'date': '2026-04-01T16:51:45.191Z', 'postedAgoShort': '17h', 'postedAgoText': '17 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "364",
    "title": "SAP Specialist",
    "company": "Deloitte South Asia",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Aziz Delhiwala",
    "status": "new",
    "posted": "{'timestamp': 1774843543578, 'date': '2026-03-30T04:05:43.578Z', 'postedAgoShort': '3d', 'postedAgoText': '3 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "365",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Kairavi Pandey",
    "status": "new",
    "posted": "{'timestamp': 1773247261432, 'date': '2026-03-11T16:41:01.432Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "366",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Muskan Sharma",
    "status": "new",
    "posted": "{'timestamp': 1775062272658, 'date': '2026-04-01T16:51:12.658Z', 'postedAgoShort': '17h', 'postedAgoText': '17 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "367",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Melanie Mehra",
    "status": "new",
    "posted": "{'timestamp': 1774550628954, 'date': '2026-03-26T18:43:48.954Z', 'postedAgoShort': '6d', 'postedAgoText': '6 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "368",
    "title": "SAP Specialist",
    "company": "Future Creation Group Of Companies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sakshi K",
    "status": "new",
    "posted": "{'timestamp': 1775119077471, 'date': '2026-04-02T08:37:57.471Z', 'postedAgoShort': '1h', 'postedAgoText': '1 hour ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "369",
    "title": "SAP Specialist",
    "company": "Dexian | Part time Hockey Skills instructor & Coach of the 2",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Colin Clapton",
    "status": "new",
    "posted": "{'timestamp': 1773846312004, 'date': '2026-03-18T15:05:12.004Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "370",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Amit Pachpor",
    "status": "new",
    "posted": "{'timestamp': 1775059305242, 'date': '2026-04-01T16:01:45.242Z', 'postedAgoShort': '18h', 'postedAgoText': '18 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "371",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Hemanth H",
    "status": "new",
    "posted": "{'timestamp': 1773330786570, 'date': '2026-03-12T15:53:06.570Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "372",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "William Roske",
    "status": "new",
    "posted": "{'timestamp': 1773763124501, 'date': '2026-03-17T15:58:44.501Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "373",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Aparna K.",
    "status": "new",
    "posted": "{'timestamp': 1775058753185, 'date': '2026-04-01T15:52:33.185Z', 'postedAgoShort': '18h', 'postedAgoText': '18 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "374",
    "title": "SAP Specialist",
    "company": "Freedom",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Gordon Macleod CEng MIET",
    "status": "new",
    "posted": "{'timestamp': 1775069682011, 'date': '2026-04-01T18:54:42.011Z', 'postedAgoShort': '15h', 'postedAgoText': '15 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "375",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Mritunjay Kumar",
    "status": "new",
    "posted": "{'timestamp': 1774469719942, 'date': '2026-03-25T20:15:19.942Z', 'postedAgoShort': '1w', 'postedAgoText': '1 week ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "376",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Rajinikanth Lakka",
    "status": "new",
    "posted": "{'timestamp': 1774533600063, 'date': '2026-03-26T14:00:00.063Z', 'postedAgoShort': '6d', 'postedAgoText': '6 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "377",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sneha Kale",
    "status": "new",
    "posted": "{'timestamp': 1773404365861, 'date': '2026-03-13T12:19:25.861Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "378",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Manjusha M",
    "status": "new",
    "posted": "{'timestamp': 1775102806716, 'date': '2026-04-02T04:06:46.716Z', 'postedAgoShort': '6h', 'postedAgoText': '6 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "379",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Becky Hardesty, PMP",
    "status": "new",
    "posted": "{'timestamp': 1775051387564, 'date': '2026-04-01T13:49:47.564Z', 'postedAgoShort': '20h', 'postedAgoText': '20 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "380",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Deepa Sharma",
    "status": "new",
    "posted": "{'timestamp': 1774914106130, 'date': '2026-03-30T23:41:46.130Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "381",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Khushi Garg",
    "status": "new",
    "posted": "{'timestamp': 1775113950842, 'date': '2026-04-02T07:12:30.842Z', 'postedAgoShort': '2h', 'postedAgoText': '2 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "382",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Roopali Charak",
    "status": "new",
    "posted": "{'timestamp': 1774532091913, 'date': '2026-03-26T13:34:51.913Z', 'postedAgoShort': '6d', 'postedAgoText': '6 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "383",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Victor Rodgers MPH BSIE RAC MBB",
    "status": "new",
    "posted": "{'timestamp': 1775043789133, 'date': '2026-04-01T11:43:09.133Z', 'postedAgoShort': '22h', 'postedAgoText': '22 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "384",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sakshi Jain",
    "status": "new",
    "posted": "{'timestamp': 1774942878246, 'date': '2026-03-31T07:41:18.246Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "385",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Varun Tej",
    "status": "new",
    "posted": "{'timestamp': 1775057838652, 'date': '2026-04-01T15:37:18.652Z', 'postedAgoShort': '18h', 'postedAgoText': '18 hours ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "386",
    "title": "SAP Specialist",
    "company": "Kabeer Consulting Inc.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Shital P.",
    "status": "new",
    "posted": "{'timestamp': 1773865279195, 'date': '2026-03-18T20:21:19.195Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "387",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nitin Miranda",
    "status": "new",
    "posted": "{'timestamp': 1774567541414, 'date': '2026-03-26T23:25:41.414Z', 'postedAgoShort': '6d', 'postedAgoText': '6 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "388",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Everita Blanchette",
    "status": "new",
    "posted": "{'timestamp': 1773298681713, 'date': '2026-03-12T06:58:01.713Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "389",
    "title": "SAP Specialist",
    "company": "BlueRock Resources | \ud83d\udc8eSmarter Hiring in SAP, DATA & AI. Lowe",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Zane Grieve-Fitzell",
    "status": "new",
    "posted": "{'timestamp': 1773674107788, 'date': '2026-03-16T15:15:07.788Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "390",
    "title": "SAP Specialist",
    "company": "Vrata Tech Solutions (VTS), An Arvind Mafatlal Group Co.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Natasha Caldeira",
    "status": "new",
    "posted": "{'timestamp': 1774872287941, 'date': '2026-03-30T12:04:47.941Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "391",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "VenkateswaraRao S",
    "status": "new",
    "posted": "{'timestamp': 1775055833960, 'date': '2026-04-01T15:03:53.960Z', 'postedAgoShort': '19h', 'postedAgoText': '19 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "392",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ajit Deshpande",
    "status": "new",
    "posted": "{'timestamp': 1772831853696, 'date': '2026-03-06T21:17:33.696Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "393",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "sakshi jadhav",
    "status": "new",
    "posted": "{'timestamp': 1774873104323, 'date': '2026-03-30T12:18:24.323Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "394",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Mohammed Hussain Shariff",
    "status": "new",
    "posted": "{'timestamp': 1774900387564, 'date': '2026-03-30T19:53:07.564Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "395",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "PYVITAL",
    "status": "new",
    "posted": "{'timestamp': 1775120405614, 'date': '2026-04-02T09:00:05.614Z', 'postedAgoShort': '1h', 'postedAgoText': '1 hour ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "396",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ajit Deshpande",
    "status": "new",
    "posted": "{'timestamp': 1773341373935, 'date': '2026-03-12T18:49:33.935Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "397",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "M Putrarani",
    "status": "new",
    "posted": "{'timestamp': 1774521755953, 'date': '2026-03-26T10:42:35.953Z', 'postedAgoShort': '6d', 'postedAgoText': '6 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "398",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Paul Marrero",
    "status": "new",
    "posted": "{'timestamp': 1773360469777, 'date': '2026-03-13T00:07:49.777Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "399",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "VOXE",
    "status": "new",
    "posted": "{'timestamp': 1773052980794, 'date': '2026-03-09T10:43:00.794Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "400",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Rahul Kumar",
    "status": "new",
    "posted": "{'timestamp': 1775121698708, 'date': '2026-04-02T09:21:38.708Z', 'postedAgoShort': '46m', 'postedAgoText': '46 minutes ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "401",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "P Hridesh",
    "status": "new",
    "posted": "{'timestamp': 1774884933527, 'date': '2026-03-30T15:35:33.527Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "402",
    "title": "SAP Specialist",
    "company": "Matlen Silver",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Anthony F.",
    "status": "new",
    "posted": "{'timestamp': 1773256926995, 'date': '2026-03-11T19:22:06.995Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "403",
    "title": "SAP Specialist",
    "company": "harish.p@thoughtwavesoft.com",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Harish Ponnam",
    "status": "new",
    "posted": "{'timestamp': 1773259533799, 'date': '2026-03-11T20:05:33.799Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "404",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jagannath Kumar",
    "status": "new",
    "posted": "{'timestamp': 1773667576973, 'date': '2026-03-16T13:26:16.973Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "405",
    "title": "SAP Specialist",
    "company": "Kerlam Technology | IT Management & Process Improvement |",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Usha Kerlam",
    "status": "new",
    "posted": "{'timestamp': 1774634245866, 'date': '2026-03-27T17:57:25.866Z', 'postedAgoShort': '5d', 'postedAgoText': '5 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "406",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Pavani N",
    "status": "new",
    "posted": "{'timestamp': 1775038021268, 'date': '2026-04-01T10:07:01.268Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "407",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Narasimha Simha",
    "status": "new",
    "posted": "{'timestamp': 1774968586244, 'date': '2026-03-31T14:49:46.244Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "408",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ashish Burle",
    "status": "new",
    "posted": "{'timestamp': 1775042914358, 'date': '2026-04-01T11:28:34.358Z', 'postedAgoShort': '22h', 'postedAgoText': '22 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "409",
    "title": "SAP Specialist",
    "company": "InterEx Group",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Madeline Brady",
    "status": "new",
    "posted": "{'timestamp': 1773415431885, 'date': '2026-03-13T15:23:51.885Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "410",
    "title": "SAP Specialist",
    "company": "a time",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Vidhyu Rao",
    "status": "new",
    "posted": "{'timestamp': 1774625926634, 'date': '2026-03-27T15:38:46.634Z', 'postedAgoShort': '5d', 'postedAgoText': '5 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "411",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Emma Adams",
    "status": "new",
    "posted": "{'timestamp': 1775032212061, 'date': '2026-04-01T08:30:12.061Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "412",
    "title": "SAP Specialist",
    "company": "ReadPointe Inc",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Murali Krishna Tummala",
    "status": "new",
    "posted": "{'timestamp': 1775055251952, 'date': '2026-04-01T14:54:11.952Z', 'postedAgoShort': '19h', 'postedAgoText': '19 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "413",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Giri Gowda T.G",
    "status": "new",
    "posted": "{'timestamp': 1775040129515, 'date': '2026-04-01T10:42:09.515Z', 'postedAgoShort': '23h', 'postedAgoText': '23 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "414",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sophia (Anu) Singh",
    "status": "new",
    "posted": "{'timestamp': 1773854141553, 'date': '2026-03-18T17:15:41.553Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "415",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "FAIR Consulting Group",
    "status": "new",
    "posted": "{'timestamp': 1775112495940, 'date': '2026-04-02T06:48:15.940Z', 'postedAgoShort': '3h', 'postedAgoText': '3 hours ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "416",
    "title": "SAP Specialist",
    "company": "YASH Technologies | Connecting Top SAP Talent with Exception",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Samiksha Dubey",
    "status": "new",
    "posted": "{'timestamp': 1775116325076, 'date': '2026-04-02T07:52:05.076Z', 'postedAgoShort': '2h', 'postedAgoText': '2 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "417",
    "title": "SAP Specialist",
    "company": "Intellect Bizware Services Pvt Ltd. | SAP",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sana Bagwan",
    "status": "new",
    "posted": "{'timestamp': 1774869574869, 'date': '2026-03-30T11:19:34.869Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "418",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sharada Challa",
    "status": "new",
    "posted": "{'timestamp': 1775113255033, 'date': '2026-04-02T07:00:55.033Z', 'postedAgoShort': '3h', 'postedAgoText': '3 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "419",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Melanie Mehra",
    "status": "new",
    "posted": "{'timestamp': 1773843046985, 'date': '2026-03-18T14:10:46.985Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "420",
    "title": "SAP Specialist",
    "company": "Infosys | Ex- Cognizant |",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Deepak Dupaguntla",
    "status": "new",
    "posted": "{'timestamp': 1774766851272, 'date': '2026-03-29T06:47:31.272Z', 'postedAgoShort': '4d', 'postedAgoText': '4 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "421",
    "title": "SAP Specialist",
    "company": "Bristlecone- A Mahindra Group Company",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Alok Adhikari",
    "status": "new",
    "posted": "{'timestamp': 1773727370522, 'date': '2026-03-17T06:02:50.522Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "422",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sanjay Singh Katheria",
    "status": "new",
    "posted": "{'timestamp': 1775111709915, 'date': '2026-04-02T06:35:09.915Z', 'postedAgoShort': '3h', 'postedAgoText': '3 hours ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "423",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Cyntia Jones, MPA, PMP, RTE",
    "status": "new",
    "posted": "{'timestamp': 1773860845190, 'date': '2026-03-18T19:07:25.190Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "424",
    "title": "SAP Specialist",
    "company": "Capgemini | Sourcing | Headhunting | CBI",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Rana Magdy",
    "status": "new",
    "posted": "{'timestamp': 1775058691108, 'date': '2026-04-01T15:51:31.108Z', 'postedAgoShort': '18h', 'postedAgoText': '18 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "425",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Bagas Adhi Kumoro Setio Wibisono",
    "status": "new",
    "posted": "{'timestamp': 1773116198191, 'date': '2026-03-10T04:16:38.191Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "426",
    "title": "SAP Specialist",
    "company": "Softtrix Tech Solutions Pvt Ltd",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sadhana Patil",
    "status": "new",
    "posted": "{'timestamp': 1775119159138, 'date': '2026-04-02T08:39:19.138Z', 'postedAgoShort': '1h', 'postedAgoText': '1 hour ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "427",
    "title": "SAP Specialist",
    "company": "Delta System & Software, Inc.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Amit kumar",
    "status": "new",
    "posted": "{'timestamp': 1774944292873, 'date': '2026-03-31T08:04:52.873Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "428",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Katia Choquette",
    "status": "new",
    "posted": "{'timestamp': 1774999801181, 'date': '2026-03-31T23:30:01.181Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "429",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Pavithra M",
    "status": "new",
    "posted": "{'timestamp': 1775050065562, 'date': '2026-04-01T13:27:45.562Z', 'postedAgoShort': '20h', 'postedAgoText': '20 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "430",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Prakhar yadav",
    "status": "new",
    "posted": "{'timestamp': 1773842473039, 'date': '2026-03-18T14:01:13.039Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "431",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Muskaan Khatoon",
    "status": "new",
    "posted": "{'timestamp': 1773640880766, 'date': '2026-03-16T06:01:20.766Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "432",
    "title": "SAP Specialist",
    "company": "Infosys",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sanjana Malik",
    "status": "new",
    "posted": "{'timestamp': 1773288893871, 'date': '2026-03-12T04:14:53.871Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "433",
    "title": "SAP Specialist",
    "company": "Pianeta Solutions | Full Cycle Recruitment Strategist | Tale",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Munish Thakur",
    "status": "new",
    "posted": "{'timestamp': 1774024225655, 'date': '2026-03-20T16:30:25.655Z', 'postedAgoShort': '1w', 'postedAgoText': '1 week ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "434",
    "title": "SAP Specialist",
    "company": "Infotics | Connecting Top Talent with Strategic Opportunitie",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Monika Swain",
    "status": "new",
    "posted": "{'timestamp': 1774582743603, 'date': '2026-03-27T03:39:03.603Z', 'postedAgoShort': '6d', 'postedAgoText': '6 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "435",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Mohammad Khaleel Uzair",
    "status": "new",
    "posted": "{'timestamp': 1772921660535, 'date': '2026-03-07T22:14:20.535Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "436",
    "title": "SAP Specialist",
    "company": "Whitehall Resources",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nicola Saxham",
    "status": "new",
    "posted": "{'timestamp': 1774979203849, 'date': '2026-03-31T17:46:43.849Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "437",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Renuka Shah",
    "status": "new",
    "posted": "{'timestamp': 1775044001668, 'date': '2026-04-01T11:46:41.668Z', 'postedAgoShort': '22h', 'postedAgoText': '22 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "438",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Amer Ali",
    "status": "new",
    "posted": "{'timestamp': 1774958433854, 'date': '2026-03-31T12:00:33.854Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "439",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sowmiya Sakthi",
    "status": "new",
    "posted": "{'timestamp': 1774938723070, 'date': '2026-03-31T06:32:03.070Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "440",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Kris Infotech Sdn Bhd",
    "status": "new",
    "posted": "{'timestamp': 1775043377334, 'date': '2026-04-01T11:36:17.334Z', 'postedAgoShort': '22h', 'postedAgoText': '22 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "441",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jennifer Sosa Eskenazi",
    "status": "new",
    "posted": "{'timestamp': 1773833181248, 'date': '2026-03-18T11:26:21.248Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "442",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ajitesh Nakka",
    "status": "new",
    "posted": "{'timestamp': 1772725765747, 'date': '2026-03-05T15:49:25.747Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "443",
    "title": "SAP Specialist",
    "company": "GraceMark Solutions || USA || CANADA || LATAM || EU || APAC",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Aviral Singh",
    "status": "new",
    "posted": "{'timestamp': 1773871778527, 'date': '2026-03-18T22:09:38.527Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "444",
    "title": "SAP Specialist",
    "company": "Tekgence",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Shivam Kashyap",
    "status": "new",
    "posted": "{'timestamp': 1773677440807, 'date': '2026-03-16T16:10:40.807Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "445",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sonali More",
    "status": "new",
    "posted": "{'timestamp': 1775042677629, 'date': '2026-04-01T11:24:37.629Z', 'postedAgoShort': '22h', 'postedAgoText': '22 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "446",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Hemant Rawat",
    "status": "new",
    "posted": "{'timestamp': 1773345136314, 'date': '2026-03-12T19:52:16.314Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "447",
    "title": "SAP Specialist",
    "company": "Investigo & Definia | SAP ERP | S/4HANA",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Lewis Dunn",
    "status": "new",
    "posted": "{'timestamp': 1774622648394, 'date': '2026-03-27T14:44:08.394Z', 'postedAgoShort': '5d', 'postedAgoText': '5 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "448",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "LASSELSBERGER Group",
    "status": "new",
    "posted": "{'timestamp': 1775043400541, 'date': '2026-04-01T11:36:40.541Z', 'postedAgoShort': '22h', 'postedAgoText': '22 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "449",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Suhayra D.",
    "status": "new",
    "posted": "{'timestamp': 1774960481013, 'date': '2026-03-31T12:34:41.013Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "450",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Siddharth Kanta",
    "status": "new",
    "posted": "{'timestamp': 1775073398937, 'date': '2026-04-01T19:56:38.937Z', 'postedAgoShort': '14h', 'postedAgoText': '14 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "451",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Janejira Laobuaban",
    "status": "new",
    "posted": "{'timestamp': 1775111074906, 'date': '2026-04-02T06:24:34.906Z', 'postedAgoShort': '3h', 'postedAgoText': '3 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "452",
    "title": "SAP Specialist",
    "company": "PRECISION ENTERPRISE",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Varsha Mavani",
    "status": "new",
    "posted": "{'timestamp': 1773587803123, 'date': '2026-03-15T15:16:43.123Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "453",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Arshad Shaik",
    "status": "new",
    "posted": "{'timestamp': 1773066271915, 'date': '2026-03-09T14:24:31.915Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "454",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Akanksha Mengi",
    "status": "new",
    "posted": "{'timestamp': 1774946642700, 'date': '2026-03-31T08:44:02.700Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "455",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Monika Pandey",
    "status": "new",
    "posted": "{'timestamp': 1774469064432, 'date': '2026-03-25T20:04:24.432Z', 'postedAgoShort': '1w', 'postedAgoText': '1 week ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "456",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Namrata Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1773400702869, 'date': '2026-03-13T11:18:22.869Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "457",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Manna Harshavardhana (VRN Technologies)",
    "status": "new",
    "posted": "{'timestamp': 1773179079628, 'date': '2026-03-10T21:44:39.628Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "458",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Krishna Sameera V",
    "status": "new",
    "posted": "{'timestamp': 1775024387355, 'date': '2026-04-01T06:19:47.355Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "459",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Dane Dan",
    "status": "new",
    "posted": "{'timestamp': 1774944361022, 'date': '2026-03-31T08:06:01.022Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "460",
    "title": "SAP Specialist",
    "company": "Airdit | HR, Performance Management",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Soumitri Das",
    "status": "new",
    "posted": "{'timestamp': 1774946974799, 'date': '2026-03-31T08:49:34.799Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "461",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "laxman Dasari",
    "status": "new",
    "posted": "{'timestamp': 1775060700211, 'date': '2026-04-01T16:25:00.211Z', 'postedAgoShort': '17h', 'postedAgoText': '17 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "462",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nitin Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1772985934422, 'date': '2026-03-08T16:05:34.422Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "463",
    "title": "SAP Specialist",
    "company": "PT. Astra Graphia Information Technology (AGIT) | Tech Recru",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Rayi Putri Rahmita Utami",
    "status": "new",
    "posted": "{'timestamp': 1775025630805, 'date': '2026-04-01T06:40:30.805Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "464",
    "title": "SAP Specialist",
    "company": "Delta System & Software, Inc. | MSc in Computer Science",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jay Suresh Chauhan",
    "status": "new",
    "posted": "{'timestamp': 1774546941060, 'date': '2026-03-26T17:42:21.060Z', 'postedAgoShort': '6d', 'postedAgoText': '6 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "465",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Abhinav Sharma",
    "status": "new",
    "posted": "{'timestamp': 1774531788729, 'date': '2026-03-26T13:29:48.729Z', 'postedAgoShort': '6d', 'postedAgoText': '6 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "466",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "John Smith",
    "status": "new",
    "posted": "{'timestamp': 1772651464165, 'date': '2026-03-04T19:11:04.165Z', 'postedAgoShort': '4w', 'postedAgoText': '0 months ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "467",
    "title": "SAP Specialist",
    "company": "Baranwal Consultancy and Services",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Prachi Kadam",
    "status": "new",
    "posted": "{'timestamp': 1774675492324, 'date': '2026-03-28T05:24:52.324Z', 'postedAgoShort': '5d', 'postedAgoText': '5 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "468",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sayma Alim",
    "status": "new",
    "posted": "{'timestamp': 1774462262650, 'date': '2026-03-25T18:11:02.650Z', 'postedAgoShort': '1w', 'postedAgoText': '1 week ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "469",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Mahesh Patel",
    "status": "new",
    "posted": "{'timestamp': 1772549174960, 'date': '2026-03-03T14:46:14.960Z', 'postedAgoShort': '4w', 'postedAgoText': '0 months ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "470",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Chakradhara Arun T.",
    "status": "new",
    "posted": "{'timestamp': 1775050072991, 'date': '2026-04-01T13:27:52.991Z', 'postedAgoShort': '20h', 'postedAgoText': '20 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "471",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Devansh Kumar",
    "status": "new",
    "posted": "{'timestamp': 1775053246499, 'date': '2026-04-01T14:20:46.499Z', 'postedAgoShort': '19h', 'postedAgoText': '19 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "472",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nitin Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1774712774439, 'date': '2026-03-28T15:46:14.439Z', 'postedAgoShort': '4d', 'postedAgoText': '4 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "473",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "BK Pandey",
    "status": "new",
    "posted": "{'timestamp': 1775028344204, 'date': '2026-04-01T07:25:44.204Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "474",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Abinaya Jagdish",
    "status": "new",
    "posted": "{'timestamp': 1775020347414, 'date': '2026-04-01T05:12:27.414Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "475",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Harshitha B K",
    "status": "new",
    "posted": "{'timestamp': 1774677964014, 'date': '2026-03-28T06:06:04.014Z', 'postedAgoShort': '5d', 'postedAgoText': '5 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "476",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nitin Jadhav",
    "status": "new",
    "posted": "{'timestamp': 1775063318834, 'date': '2026-04-01T17:08:38.834Z', 'postedAgoShort': '16h', 'postedAgoText': '16 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "477",
    "title": "SAP Specialist",
    "company": "FC Group Of Companies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Avinash Dhane",
    "status": "new",
    "posted": "{'timestamp': 1774711175092, 'date': '2026-03-28T15:19:35.092Z', 'postedAgoShort': '4d', 'postedAgoText': '4 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "478",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Callum George",
    "status": "new",
    "posted": "{'timestamp': 1774936808229, 'date': '2026-03-31T06:00:08.229Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "479",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sana Asher",
    "status": "new",
    "posted": "{'timestamp': 1775048486670, 'date': '2026-04-01T13:01:26.670Z', 'postedAgoShort': '21h', 'postedAgoText': '21 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "480",
    "title": "SAP Specialist",
    "company": "Circle - Specialising in Digital Transformation, Pharmaceuti",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Yolanda Fiuza",
    "status": "new",
    "posted": "{'timestamp': 1772627927337, 'date': '2026-03-04T12:38:47.337Z', 'postedAgoShort': '4w', 'postedAgoText': '0 months ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "481",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jan Sirirat",
    "status": "new",
    "posted": "{'timestamp': 1773199925110, 'date': '2026-03-11T03:32:05.110Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "482",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Indi Kitaure",
    "status": "new",
    "posted": "{'timestamp': 1775023225442, 'date': '2026-04-01T06:00:25.442Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "483",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sachin Sharma",
    "status": "new",
    "posted": "{'timestamp': 1773677371724, 'date': '2026-03-16T16:09:31.724Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "484",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Kuldeep Arya",
    "status": "new",
    "posted": "{'timestamp': 1773745956200, 'date': '2026-03-17T11:12:36.200Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "485",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Abhay Singh",
    "status": "new",
    "posted": "{'timestamp': 1774875746586, 'date': '2026-03-30T13:02:26.586Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "486",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Fazal N.",
    "status": "new",
    "posted": "{'timestamp': 1775052902353, 'date': '2026-04-01T14:15:02.353Z', 'postedAgoShort': '19h', 'postedAgoText': '19 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "487",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Badarinadh Gelli",
    "status": "new",
    "posted": "{'timestamp': 1774931402978, 'date': '2026-03-31T04:30:02.978Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "488",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Pallavi G.",
    "status": "new",
    "posted": "{'timestamp': 1773638886151, 'date': '2026-03-16T05:28:06.151Z', 'postedAgoShort': '2w', 'postedAgoText': '2 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "489",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Daniel Ross",
    "status": "new",
    "posted": "{'timestamp': 1774942208216, 'date': '2026-03-31T07:30:08.216Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "490",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "ConSAP",
    "status": "new",
    "posted": "{'timestamp': 1775081748616, 'date': '2026-04-01T22:15:48.616Z', 'postedAgoShort': '11h', 'postedAgoText': '11 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "491",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sachin Sharma",
    "status": "new",
    "posted": "{'timestamp': 1773072184043, 'date': '2026-03-09T16:03:04.043Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "492",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Jean Shaw, MHRM",
    "status": "new",
    "posted": "{'timestamp': 1775079962115, 'date': '2026-04-01T21:46:02.115Z', 'postedAgoShort': '12h', 'postedAgoText': '12 hours ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "493",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ana Monteiro",
    "status": "new",
    "posted": "{'timestamp': 1774990455852, 'date': '2026-03-31T20:54:15.852Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "494",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Luis R. Orecchia",
    "status": "new",
    "posted": "{'timestamp': 1774962967949, 'date': '2026-03-31T13:16:07.949Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "495",
    "title": "SAP Specialist",
    "company": "Scale Project Leadership | SAP | Microsoft | Cloud | FSCP | ",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Ivan Snell",
    "status": "new",
    "posted": "{'timestamp': 1775033987347, 'date': '2026-04-01T08:59:47.347Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "496",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "MICKAEL QUESNOT",
    "status": "new",
    "posted": "{'timestamp': 1774867148001, 'date': '2026-03-30T10:39:08.001Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "497",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Wouter van Heddeghem",
    "status": "new",
    "posted": "{'timestamp': 1774974387007, 'date': '2026-03-31T16:26:27.007Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Edited \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "498",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Project School",
    "status": "new",
    "posted": "{'timestamp': 1774942663587, 'date': '2026-03-31T07:37:43.587Z', 'postedAgoShort': '2d', 'postedAgoText': '2 days ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "499",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "MICKAEL QUESNOT",
    "status": "new",
    "posted": "{'timestamp': 1775105101705, 'date': '2026-04-02T04:45:01.705Z', 'postedAgoShort': '5h', 'postedAgoText': '5 hours ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "500",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Abhay Singh",
    "status": "new",
    "posted": "{'timestamp': 1775021473398, 'date': '2026-04-01T05:31:13.398Z', 'postedAgoShort': '1d', 'postedAgoText': '1 day ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "501",
    "title": "SAP Specialist",
    "company": "Direct Recruiter",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sachin Sharma",
    "status": "new",
    "posted": "{'timestamp': 1773075426577, 'date': '2026-03-09T16:57:06.577Z', 'postedAgoShort': '3w', 'postedAgoText': '3 weeks ago \u2022 Visible to anyone on or off LinkedIn'}"
  },
  {
    "id": "502",
    "title": "SAP Specialist",
    "company": "VGreen Technology Solutions (VGreenTEK)",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "VGreen Technology Solutions (VGreenTEK)",
    "status": "new",
    "posted": ""
  },
  {
    "id": "503",
    "title": "SAP Specialist",
    "company": "DigiHelic Solutions Pvt. Ltd.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "DigiHelic Solutions Pvt. Ltd.",
    "status": "new",
    "posted": ""
  },
  {
    "id": "504",
    "title": "SAP Specialist",
    "company": "NEC Smart Cities",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "NEC Smart Cities",
    "status": "new",
    "posted": ""
  },
  {
    "id": "505",
    "title": "SAP Specialist",
    "company": "DigiHelic Solutions Pvt. Ltd.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "DigiHelic Solutions Pvt. Ltd.",
    "status": "new",
    "posted": ""
  },
  {
    "id": "506",
    "title": "SAP Specialist",
    "company": "DigiHelic Solutions Pvt. Ltd.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "DigiHelic Solutions Pvt. Ltd.",
    "status": "new",
    "posted": ""
  },
  {
    "id": "507",
    "title": "SAP Specialist",
    "company": "FullStack",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "FullStack",
    "status": "new",
    "posted": ""
  },
  {
    "id": "508",
    "title": "SAP Specialist",
    "company": "Sloka IT Solutions",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Sloka IT Solutions",
    "status": "new",
    "posted": ""
  },
  {
    "id": "509",
    "title": "SAP Specialist",
    "company": "NTT DATA Business Solutions",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "NTT DATA Business Solutions",
    "status": "new",
    "posted": ""
  },
  {
    "id": "510",
    "title": "SAP Specialist",
    "company": "YASH Technologies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "YASH Technologies",
    "status": "new",
    "posted": ""
  },
  {
    "id": "511",
    "title": "SAP Specialist",
    "company": "Westernacher Consulting",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Westernacher Consulting",
    "status": "new",
    "posted": ""
  },
  {
    "id": "512",
    "title": "SAP Specialist",
    "company": "RAYVEN IT SOLUTIONS",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "RAYVEN IT SOLUTIONS",
    "status": "new",
    "posted": ""
  },
  {
    "id": "513",
    "title": "SAP Specialist",
    "company": "WMS - Global",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "WMS - Global",
    "status": "new",
    "posted": ""
  },
  {
    "id": "514",
    "title": "SAP Specialist",
    "company": "Codem Inc.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Codem Inc.",
    "status": "new",
    "posted": ""
  },
  {
    "id": "515",
    "title": "SAP Specialist",
    "company": "Coforge",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Coforge",
    "status": "new",
    "posted": ""
  },
  {
    "id": "516",
    "title": "SAP Specialist",
    "company": "DigiHelic Solutions Pvt. Ltd.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "DigiHelic Solutions Pvt. Ltd.",
    "status": "new",
    "posted": ""
  },
  {
    "id": "517",
    "title": "SAP Specialist",
    "company": "KAMKON IT SOLUTIONS PVT LTD",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "KAMKON IT SOLUTIONS PVT LTD",
    "status": "new",
    "posted": ""
  },
  {
    "id": "518",
    "title": "SAP Specialist",
    "company": "Komodo Health",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Komodo Health",
    "status": "new",
    "posted": ""
  },
  {
    "id": "519",
    "title": "SAP Specialist",
    "company": "Westernacher Consulting",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Westernacher Consulting",
    "status": "new",
    "posted": ""
  },
  {
    "id": "520",
    "title": "SAP Specialist",
    "company": "Lorven Technologies Inc.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Lorven Technologies Inc.",
    "status": "new",
    "posted": ""
  },
  {
    "id": "521",
    "title": "SAP Specialist",
    "company": "CYAN360",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "CYAN360",
    "status": "new",
    "posted": ""
  },
  {
    "id": "522",
    "title": "SAP Specialist",
    "company": "Westernacher Consulting",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Westernacher Consulting",
    "status": "new",
    "posted": ""
  },
  {
    "id": "523",
    "title": "SAP Specialist",
    "company": "Fusion Consulting",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Fusion Consulting",
    "status": "new",
    "posted": ""
  },
  {
    "id": "524",
    "title": "SAP Specialist",
    "company": "Fusion Consulting",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Fusion Consulting",
    "status": "new",
    "posted": ""
  },
  {
    "id": "525",
    "title": "SAP Specialist",
    "company": "Decskill",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Decskill",
    "status": "new",
    "posted": ""
  },
  {
    "id": "526",
    "title": "SAP Specialist",
    "company": "Westernacher Consulting",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Westernacher Consulting",
    "status": "new",
    "posted": ""
  },
  {
    "id": "527",
    "title": "SAP Specialist",
    "company": "NTT DATA North America",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "NTT DATA North America",
    "status": "new",
    "posted": ""
  },
  {
    "id": "528",
    "title": "SAP Specialist",
    "company": "Maitsys",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Maitsys",
    "status": "new",
    "posted": ""
  },
  {
    "id": "529",
    "title": "SAP Specialist",
    "company": "WMS - Global",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "WMS - Global",
    "status": "new",
    "posted": ""
  },
  {
    "id": "530",
    "title": "SAP Specialist",
    "company": "WMS - Global",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "WMS - Global",
    "status": "new",
    "posted": ""
  },
  {
    "id": "531",
    "title": "SAP Specialist",
    "company": "Weekday AI (YC W21)",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Weekday AI (YC W21)",
    "status": "new",
    "posted": ""
  },
  {
    "id": "532",
    "title": "SAP Specialist",
    "company": "Westernacher Consulting",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Westernacher Consulting",
    "status": "new",
    "posted": ""
  },
  {
    "id": "533",
    "title": "SAP Specialist",
    "company": "Gainwell Technologies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Gainwell Technologies",
    "status": "new",
    "posted": ""
  },
  {
    "id": "534",
    "title": "SAP Specialist",
    "company": "Westernacher Consulting",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Westernacher Consulting",
    "status": "new",
    "posted": ""
  },
  {
    "id": "535",
    "title": "SAP Specialist",
    "company": "Westernacher Consulting",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Westernacher Consulting",
    "status": "new",
    "posted": ""
  },
  {
    "id": "536",
    "title": "SAP Specialist",
    "company": "Droisys",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Droisys",
    "status": "new",
    "posted": ""
  },
  {
    "id": "537",
    "title": "SAP Specialist",
    "company": "RAPSYS TECHNOLOGIES PTE LTD",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "RAPSYS TECHNOLOGIES PTE LTD",
    "status": "new",
    "posted": ""
  },
  {
    "id": "538",
    "title": "SAP Specialist",
    "company": "Westernacher Consulting",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Westernacher Consulting",
    "status": "new",
    "posted": ""
  },
  {
    "id": "539",
    "title": "SAP Specialist",
    "company": "Tachyon Technologies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Tachyon Technologies",
    "status": "new",
    "posted": ""
  },
  {
    "id": "540",
    "title": "SAP Specialist",
    "company": "WillWare Technologies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "WillWare Technologies",
    "status": "new",
    "posted": ""
  },
  {
    "id": "541",
    "title": "SAP Specialist",
    "company": "Delta System & Software, Inc.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Delta System & Software, Inc.",
    "status": "new",
    "posted": ""
  },
  {
    "id": "542",
    "title": "SAP Specialist",
    "company": "Westernacher Consulting",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Westernacher Consulting",
    "status": "new",
    "posted": ""
  },
  {
    "id": "543",
    "title": "SAP Specialist",
    "company": "Serrala",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Serrala",
    "status": "new",
    "posted": ""
  },
  {
    "id": "544",
    "title": "SAP Specialist",
    "company": "DigiHelic Solutions Pvt. Ltd.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "DigiHelic Solutions Pvt. Ltd.",
    "status": "new",
    "posted": ""
  },
  {
    "id": "545",
    "title": "SAP Specialist",
    "company": "WillWare Technologies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "WillWare Technologies",
    "status": "new",
    "posted": ""
  },
  {
    "id": "546",
    "title": "SAP Specialist",
    "company": "Cube Hub Inc.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Cube Hub Inc.",
    "status": "new",
    "posted": ""
  },
  {
    "id": "547",
    "title": "SAP Specialist",
    "company": "KeyLynk",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "KeyLynk",
    "status": "new",
    "posted": ""
  },
  {
    "id": "548",
    "title": "SAP Specialist",
    "company": "Westernacher Consulting",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Westernacher Consulting",
    "status": "new",
    "posted": ""
  },
  {
    "id": "549",
    "title": "SAP Specialist",
    "company": "YASH Technologies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "YASH Technologies",
    "status": "new",
    "posted": ""
  },
  {
    "id": "550",
    "title": "SAP Specialist",
    "company": "Kagool",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Kagool",
    "status": "new",
    "posted": ""
  },
  {
    "id": "551",
    "title": "SAP Specialist",
    "company": "Capco",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Capco",
    "status": "new",
    "posted": ""
  },
  {
    "id": "552",
    "title": "SAP Specialist",
    "company": "Cordiso",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Cordiso",
    "status": "new",
    "posted": ""
  },
  {
    "id": "553",
    "title": "SAP Specialist",
    "company": "Cortex Consultants LLC",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Cortex Consultants LLC",
    "status": "new",
    "posted": ""
  },
  {
    "id": "554",
    "title": "SAP Specialist",
    "company": "Cortex Consultants LLC",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Cortex Consultants LLC",
    "status": "new",
    "posted": ""
  },
  {
    "id": "555",
    "title": "SAP Specialist",
    "company": "Cactus Communications",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Cactus Communications",
    "status": "new",
    "posted": ""
  },
  {
    "id": "556",
    "title": "SAP Specialist",
    "company": "Capco",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Capco",
    "status": "new",
    "posted": ""
  },
  {
    "id": "557",
    "title": "SAP Specialist",
    "company": "Blueprint Technologies Pvt Ltd",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Blueprint Technologies Pvt Ltd",
    "status": "new",
    "posted": ""
  },
  {
    "id": "558",
    "title": "SAP Specialist",
    "company": "DigiHelic Solutions Pvt. Ltd.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "DigiHelic Solutions Pvt. Ltd.",
    "status": "new",
    "posted": ""
  },
  {
    "id": "559",
    "title": "SAP Specialist",
    "company": "NTT DATA North America",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "NTT DATA North America",
    "status": "new",
    "posted": ""
  },
  {
    "id": "560",
    "title": "SAP Specialist",
    "company": "Nagarro",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nagarro",
    "status": "new",
    "posted": ""
  },
  {
    "id": "561",
    "title": "SAP Specialist",
    "company": "Akamai Technologies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Akamai Technologies",
    "status": "new",
    "posted": ""
  },
  {
    "id": "562",
    "title": "SAP Specialist",
    "company": "Capco",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Capco",
    "status": "new",
    "posted": ""
  },
  {
    "id": "563",
    "title": "SAP Specialist",
    "company": "DigitalDhara",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "DigitalDhara",
    "status": "new",
    "posted": ""
  },
  {
    "id": "564",
    "title": "SAP Specialist",
    "company": "DigiHelic Solutions Pvt. Ltd.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "DigiHelic Solutions Pvt. Ltd.",
    "status": "new",
    "posted": ""
  },
  {
    "id": "565",
    "title": "SAP Specialist",
    "company": "Agilent Technologies",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Agilent Technologies",
    "status": "new",
    "posted": ""
  },
  {
    "id": "566",
    "title": "SAP Specialist",
    "company": "Maneva Consulting Pvt. Ltd.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Maneva Consulting Pvt. Ltd.",
    "status": "new",
    "posted": ""
  },
  {
    "id": "567",
    "title": "SAP Specialist",
    "company": "Capco",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Capco",
    "status": "new",
    "posted": ""
  },
  {
    "id": "568",
    "title": "SAP Specialist",
    "company": "Avensys Consulting",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Avensys Consulting",
    "status": "new",
    "posted": ""
  },
  {
    "id": "569",
    "title": "SAP Specialist",
    "company": "Syniti",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Syniti",
    "status": "new",
    "posted": ""
  },
  {
    "id": "570",
    "title": "SAP Specialist",
    "company": "NTT DATA North America",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "NTT DATA North America",
    "status": "new",
    "posted": ""
  },
  {
    "id": "571",
    "title": "SAP Specialist",
    "company": "Nagarro",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nagarro",
    "status": "new",
    "posted": ""
  },
  {
    "id": "572",
    "title": "SAP Specialist",
    "company": "KWA Analytics",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "KWA Analytics",
    "status": "new",
    "posted": ""
  },
  {
    "id": "573",
    "title": "SAP Specialist",
    "company": "NTT DATA North America",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "NTT DATA North America",
    "status": "new",
    "posted": ""
  },
  {
    "id": "574",
    "title": "SAP Specialist",
    "company": "Nagarro",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nagarro",
    "status": "new",
    "posted": ""
  },
  {
    "id": "575",
    "title": "SAP Specialist",
    "company": "Delta System & Software, Inc.",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Delta System & Software, Inc.",
    "status": "new",
    "posted": ""
  },
  {
    "id": "576",
    "title": "SAP Specialist",
    "company": "OpenIAM",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "OpenIAM",
    "status": "new",
    "posted": ""
  },
  {
    "id": "577",
    "title": "SAP Specialist",
    "company": "Rapinno Tech Solutions GmbH",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Rapinno Tech Solutions GmbH",
    "status": "new",
    "posted": ""
  },
  {
    "id": "578",
    "title": "SAP Specialist",
    "company": "Nagarro",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Nagarro",
    "status": "new",
    "posted": ""
  },
  {
    "id": "579",
    "title": "SAP Specialist",
    "company": "Capco",
    "location": "Remote / Hybrid",
    "platform": "LinkedIn",
    "recruiter": "Capco",
    "status": "new",
    "posted": ""
  }
];

const filters = ["All", "New", "Applied", "Tailoring", "Failed"];

export default function JobFeed() {
  const [activeFilter, setActiveFilter] = useState("All");

  const filtered = activeFilter === "All" ? jobs : jobs.filter(j => j.status === activeFilter.toLowerCase());

  return (
    <div className="space-y-6 animate-slide-up">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Job Feed</h1>
          <p className="text-sm text-muted-foreground mt-1">{jobs.length} positions in pipeline</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-2 rounded-lg bg-secondary px-3 py-1.5">
            <Search className="h-3.5 w-3.5 text-muted-foreground" />
            <input type="text" placeholder="Search jobs..." className="bg-transparent text-sm text-foreground placeholder:text-muted-foreground outline-none w-40" />
          </div>
          <button className="p-2 rounded-lg bg-secondary text-muted-foreground hover:text-foreground transition-colors">
            <Filter className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-2 flex-wrap">
        {filters.map((f) => (
          <button
            key={f}
            onClick={() => setActiveFilter(f)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activeFilter === f
                ? "bg-primary/15 text-primary"
                : "bg-secondary text-muted-foreground hover:text-foreground"
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Job Cards Grid */}
      <div className="bento-grid grid-cols-1 md:grid-cols-2">
        {filtered.map((job) => {
          const status = statusConfig[job.status];
          return (
            <div key={job.id} className="glass-card-hover p-5 flex flex-col gap-4">
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <Badge variant="outline" className={`text-[10px] px-1.5 py-0 ${status.className}`}>
                      {status.label}
                    </Badge>
                    <span className="text-[10px] text-muted-foreground">{job.posted}</span>
                  </div>
                  <h3 className="font-semibold text-sm truncate">{job.title}</h3>
                </div>
                <div className="text-[10px] font-medium px-2 py-1 rounded bg-secondary text-muted-foreground shrink-0">
                  {job.platform}
                </div>
              </div>

              <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted-foreground">
                <span className="flex items-center gap-1"><Building2 className="h-3 w-3" />{job.company}</span>
                <span className="flex items-center gap-1"><MapPin className="h-3 w-3" />{job.location}</span>
                <span className="flex items-center gap-1"><User className="h-3 w-3" />{job.recruiter}</span>
              </div>

              <div className="flex items-center gap-2 mt-auto pt-2">
                <button className="flex-1 flex items-center justify-center gap-2 rounded-lg bg-success/15 px-3 py-2 text-xs font-semibold text-success transition-colors hover:bg-success/25">
                  <Sparkles className="h-3.5 w-3.5" />
                  Apply with AI
                </button>
                <button className="p-2 rounded-lg bg-secondary text-muted-foreground hover:text-foreground transition-colors">
                  <ExternalLink className="h-3.5 w-3.5" />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
