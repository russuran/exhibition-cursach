import React, { useEffect, useState } from 'react';
import { Table, Button, Modal } from 'antd';
import axios from 'axios';
import ExhibitionContentForm from '../components/ExhibitionContentForm';

const ExhibitionContents = () => {
    const [contents, setContents] = useState([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [currentContent, setCurrentContent] = useState(null);

    useEffect(() => {
        fetchContents();
    }, []);

    const fetchContents = async () => {
        const response = await axios.get('http://localhost:3001/exhibition_contents/');
        setContents(response.data);
    };

    const handleDelete = async (exhibitId, exhibitionId) => {
        await axios.delete(`http://localhost:3001/exhibition_contents/${exhibitId}/${exhibitionId}`);
        fetchContents();
    };

    const handleModalOpen = (content) => {
        setCurrentContent(content);
        setIsModalVisible(true);
    };

    const handleModalClose = () => {
        setCurrentContent(null);
        setIsModalVisible(false);
    };

    const handleFormSubmit = async (values) => {
        if (currentContent) {
            await axios.put(`http://localhost:3001/exhibition_contents/${currentContent.exhibit_id}/${currentContent.exhibition_id}`, values);
        } else {
            await axios.post('http://localhost:3001/exhibition_contents/', values);
        }
        fetchContents();
        handleModalClose();
    };

    return (
        <div>
            <Button type="primary" onClick={() => handleModalOpen(null)} style={{ marginBottom: 16 }}>
                Добавить Экспонаты на Выставку
            </Button>
            <Table dataSource={contents} rowKey={record => `${record.exhibit_id}-${record.exhibition_id}`}>
                <Table.Column title="Exhibit ID" dataIndex="exhibit_id" />
                <Table.Column title="Exhibition ID" dataIndex="exhibition_id" />
                <Table.Column title="Actions" render={(text, content) => (
                    <>
                        <Button onClick={() => handleModalOpen(content)}>Редактировать</Button>
                        <Button onClick={() => handleDelete(content.exhibit_id, content.exhibition_id)}>Удалить</Button>
                    </>
                )} />
            </Table>
            <Modal
                title={currentContent ? "Редактировать ДЭнВ" : "Добавить ДЭнВ"}
                visible={isModalVisible}
                onCancel={handleModalClose}
                footer={null}
            >
                <ExhibitionContentForm
                    initialValues={currentContent}
                    onSubmit={handleFormSubmit}
                />
            </Modal>
        </div>
    );
};

export default ExhibitionContents;
