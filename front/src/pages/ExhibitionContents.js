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
        const response = await axios.get('http://localhost:5000/exhibition_contents/');
        setContents(response.data);
    };

    const handleDelete = async (id) => {
        await axios.delete(`http://localhost:5000/exhibition_contents/${id}/`);
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
            await axios.put(`http://localhost:5000/exhibition_contents/${currentContent.id}`, values);
        } else {
            await axios.post('http://localhost:5000/exhibition_contents/', values);
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
                <Table.Column title="Выставка" dataIndex="exhibition_id" />
                <Table.Column title="Экспонат" dataIndex="exhibit_id" />
                <Table.Column title="Действия" render={(text, content) => (
                    <div style={{ display: 'flex', gap: 10 }}>
                        <Button onClick={() => handleModalOpen(content)}>Редактировать</Button>
                        <Button onClick={() => handleDelete(content.id)}>Удалить</Button>
                    </div>
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
