import React, { useEffect, useState } from 'react';
import { Table, Button, Modal } from 'antd';
import axios from 'axios';
import ExhibitionForm from '../components/ExhibitionForm';

const Exhibitions = () => {
    const [exhibitions, setExhibitions] = useState([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [currentExhibition, setCurrentExhibition] = useState(null);

    useEffect(() => {
        fetchExhibitions();
    }, []);

    const fetchExhibitions = async () => {
        const response = await axios.get('/exhibitions/');
        setExhibitions(response.data);
    };

    const handleDelete = async (exhibitionId) => {
        await axios.delete(`/exhibitions/${exhibitionId}`);
        fetchExhibitions();
    };

    const handleModalOpen = (exhibition) => {
        setCurrentExhibition(exhibition);
        setIsModalVisible(true);
    };

    const handleModalClose = () => {
        setCurrentExhibition(null);
        setIsModalVisible(false);
    };

    const handleFormSubmit = async (values) => {
        if (currentExhibition) {
            await axios.put(`http://localhost:3001/exhibitions/${currentExhibition.exhibition_id}`, values);
        } else {
            await axios.post('http://localhost:3001/exhibitions/', values);
        }
        fetchExhibitions();
        handleModalClose();
    };

    return (
        <div>
            <Button type="primary" onClick={() => handleModalOpen(null)} style={{ marginBottom: 16 }}>
                Добавить Выставку
            </Button>
            <Table dataSource={exhibitions} rowKey="exhibition_id">
                <Table.Column title="Название" dataIndex="title" />
                <Table.Column title="Описание" dataIndex="description" />
                <Table.Column title="Дата начала" dataIndex="start_date" />
                <Table.Column title="Дата окончания" dataIndex="end_date" />
                <Table.Column title="Расписание" dataIndex="working_schedule" />
                <Table.Column title="Actions" render={(text, exhibition) => (
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <Button onClick={() => handleModalOpen(exhibition)}>Редактировать</Button>
                        <Button onClick={() => handleDelete(exhibition.exhibition_id)}>Удалить</Button>
                    </div>
                )} />
            </Table>
            <Modal
                title={currentExhibition ? "Редактировать выставку" : "Добавить выставку"}
                visible={isModalVisible}
                onCancel={handleModalClose}
                footer={null}
            >
                <ExhibitionForm
                    initialValues={currentExhibition}
                    onSubmit={handleFormSubmit}
                />
            </Modal>
        </div>
    );
};

export default Exhibitions;
