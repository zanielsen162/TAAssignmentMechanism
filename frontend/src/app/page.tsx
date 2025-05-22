"use client";
import { useState } from "react";

const applicanst = [
  { name: "Applicant 1" },
  { name: "Applicant 2" },
  { name: "Applicant 3" },
];

const numberOfSlots = 3;

export default function Example() {
  const [rows, setRows] = useState([{ applicant: "", slot: null }]);
  const [selectedApplicants, setSelectedApplicants] = useState<string[]>([]);

  const handleSelectChange = (value: string, index: number) => {
    const updatedRows = [...rows];
    updatedRows[index].applicant = value;
    setRows(updatedRows);

    const updatedSelections = updatedRows.map((row) => row.applicant);
    setSelectedApplicants(updatedSelections);
  };

  const handleSlotChange = (slot: number, index: number) => {
    const updatedRows = [...rows];
    updatedRows[index].slot = slot;
    setRows(updatedRows);
  };

  const handleAddRow = () => {
    setRows([...rows, { applicant: "", slot: null }]);
  };

  const handleRemoveRow = () => {
    if (rows.length > 1) {
      const updatedRows = rows.slice(0, -1); // Remove the last row
      setRows(updatedRows);

      // Update selectedApplicants to reflect the removed row
      const updatedSelections = updatedRows.map((row) => row.applicant);
      setSelectedApplicants(updatedSelections);
    }
  };

  return (
    <div className="flex items-center justify-center mt-10">
      <form className="bg-white place-content-center shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div className="space-y-12">
          <div className="border-b border-gray-900/10 pb-12">
            <h2 className="text-base/7 font-semibold text-gray-900">Teaching Assistant Preference Form</h2>
            <p className="mt-1 text-sm/6 text-gray-600">
              Please select applicants and assign them to slots.
            </p>

            {/* Table for applicants and slots */}
            <div className="mt-10">
              <table className="table-auto w-full border-collapse border border-gray-300">
                <thead>
                  <tr>
                    <th className="border border-gray-300 px-4 py-2 text-left">Applicant</th>
                    {Array.from({ length: numberOfSlots+1 }).map((_, slotIndex) => (
                      <th key={slotIndex} className="border border-gray-300 px-4 py-2 text-center">
                        {slotIndex}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row, index) => (
                    <tr key={index}>
                      <td className="border border-gray-300 px-4 py-2">
                        <select
                          name={`applicant-${index}`}
                          value={row.applicant}
                          onChange={(e) => handleSelectChange(e.target.value, index)}
                          className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                        >
                          <option value="">Select an applicant</option>
                          {applicanst
                            .filter((applicant) => !selectedApplicants.includes(applicant.name) || row.applicant === applicant.name)
                            .map((applicant, idx) => (
                              <option key={idx} value={applicant.name}>
                                {applicant.name}
                              </option>
                            ))}
                        </select>
                      </td>
                      {Array.from({ length: numberOfSlots +1 }).map((_, slotIndex) => (
                        <td key={slotIndex} className="border border-gray-300 px-4 py-2 text-center">
                          <input
                            type="radio"
                            name={`slot-${index}`}
                            value={slotIndex}
                            checked={row.slot === slotIndex}
                            onChange={() => handleSlotChange(slotIndex, index)}
                            className="form-radio text-indigo-600 focus:ring-indigo-500"
                          />
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
              <button
                type="button"
                onClick={handleAddRow}
                className="mt-4 rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Add Row
              </button>
              <button
                type="button"
                onClick={handleRemoveRow}
                className="mt-4 rounded-md px-3 py-2 text-sm text-gray-400"
              >
                Remove Row
              </button>
            </div>
          </div>
        </div>

        <div className="mt-6 flex items-center justify-end gap-x-6">
          <button
            type="submit"
            className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  );
}
