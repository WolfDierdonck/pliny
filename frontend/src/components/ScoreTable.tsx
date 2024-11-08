import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from './ui/table';

import React from 'react';

const pageScores = [
  {
    pageName: 'Taylor Swift',
    viewScore: 99,
    editScore: 100,
    vandalismScore: 12,
    totalScore: 200,
  },
  {
    pageName: 'Kanye West',
    viewScore: 100,
    editScore: 100,
    vandalismScore: 0,
    totalScore: 200,
  },
  {
    pageName: 'Barack Obama',
    viewScore: 100,
    editScore: 100,
    vandalismScore: 0,
    totalScore: 200,
  },
  {
    pageName: 'Donald Trump',
    viewScore: 100,
    editScore: 100,
    vandalismScore: 0,
    totalScore: 200,
  },
  {
    pageName: 'Elon Musk',
    viewScore: 100,
    editScore: 100,
    vandalismScore: 0,
    totalScore: 200,
  },
];

export function ScoreTable() {
  return (
    <div className="flex size-fit items-center justify-center">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[100px]">Name</TableHead>
            <TableHead>View Score</TableHead>
            <TableHead>Edit Score</TableHead>
            <TableHead>Vandalism Score</TableHead>
            <TableHead className="text-right">Total Score</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {pageScores.map((pageScore) => (
            <TableRow key={pageScore.pageName}>
              <TableCell className="font-medium">
                {pageScore.pageName}
              </TableCell>
              <TableCell>{pageScore.viewScore}</TableCell>
              <TableCell>{pageScore.editScore}</TableCell>
              <TableCell>{pageScore.vandalismScore}</TableCell>
              <TableCell className="text-right">
                {pageScore.totalScore}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
