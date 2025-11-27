import { Trash2 } from 'lucide-react';

const DeleteConfirmDialog = ({ isOpen, onConfirm, onCancel, itemType, itemCount }) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full mx-4">
                <div className="flex items-center mb-4">
                    <div className="p-2 bg-red-100 rounded-full text-red-600 mr-3">
                        <Trash2 size={24} />
                    </div>
                    <h2 className="text-xl font-semibold text-gray-800">Element löschen?</h2>
                </div>

                <p className="text-gray-600 mb-6">
                    Möchten Sie wirklich {itemCount > 1 ? `${itemCount} ${itemType}s` : `diesen ${itemType}`} löschen?
                    {itemType === 'Node' && ' Alle verbundenen Edges werden ebenfalls gelöscht.'}
                </p>

                <div className="flex justify-end space-x-3">
                    <button
                        onClick={onCancel}
                        className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors"
                    >
                        Abbrechen
                    </button>
                    <button
                        onClick={onConfirm}
                        className="px-4 py-2 bg-red-600 rounded-md hover:bg-red-700 transition-colors"
                    >
                        Löschen
                    </button>
                </div>
            </div>
        </div>
    );
};

export default DeleteConfirmDialog;
